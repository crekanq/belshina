from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from chats.models import Chat
from .forms import LoginForm, RegisterForm


class UserLoginView(View):
    template_name = 'users/login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')  # Redirect если user авторизован
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect после авторизации
        return render(request, self.template_name, {'form': form})


class UserRegisterView(View):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')  # Redirect если user авторизован
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            common_chat, created = Chat.objects.get_or_create()
            common_chat.users.add(user)
            login(request, user)
            return redirect('login')  # Redirect после регистрации
        return render(request, self.template_name, {'form': form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
