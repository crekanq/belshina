from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from .forms import MessageForm
from .models import Chat, Message


class CreateChatView(UserPassesTestMixin, View):
    template_name = 'chats/create_chat.html'

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('login')

    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        return render(request, self.template_name, {'users': users})

    def post(self, request):
        selected_users_ids = request.POST.getlist('selected_users')
        users = User.objects.filter(id__in=selected_users_ids)

        if not users:
            users = User.objects.exclude(id=request.user.id)
            return render(request, self.template_name, {
                'users': users,
                'error_message': 'Выберите хотя бы одного пользователя для создания чата'
            })

        chat = Chat.objects.create(name=request.POST.get('chat_name'))
        chat.users.add(request.user, *users)
        return redirect('/')


class ChatView(UserPassesTestMixin, View):
    template_name = 'chats/chat.html'

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('login')

    def get(self, request):
        user_chats = Chat.objects.filter(users=request.user)
        message_form = MessageForm()
        return render(request, self.template_name, {'chats': user_chats, 'message_form': message_form})

    def post(self, request):
        if 'toggle_chat' in request.POST:
            chat_id = request.POST.get('chat_id')
            self.toggle_chat_visibility(chat_id)
            return redirect('chat')

        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            content = message_form.cleaned_data['content']
            chat_id = message_form.cleaned_data['chat_id']
            chat = Chat.objects.get(id=chat_id)
            Message.objects.create(chat=chat, sender=request.user, content=content)
        else:
            print(message_form.errors)

        return redirect('chat')

    def toggle_chat_visibility(self, chat_id):
        chat = Chat.objects.get(id=chat_id)
        chat.hidden = not chat.hidden
        chat.save()

