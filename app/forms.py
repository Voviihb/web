from django import forms

from app.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    class Meta:
        user = UserProfile
