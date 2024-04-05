from django import forms


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    chat_id = forms.IntegerField(widget=forms.HiddenInput())
