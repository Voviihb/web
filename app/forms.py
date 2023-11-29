from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(),
        min_length=6
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.save()

        profile = UserProfile(user=user)

        if commit:
            profile.save()

        return user
