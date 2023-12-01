from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

from app.models import UserProfile, Question, Tag


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


class UserProfileForm(UserChangeForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'avatar']


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}),
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.user = user

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class AskForm(forms.ModelForm):
    tags = forms.CharField(
        label="Enter tags (', '-separated)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    title = forms.CharField(
        label="Title",
        strip=True,
        required=True,
        min_length=10
    )

    content = forms.CharField(
        label="Describe your question",
        strip=True,
        required=True,
        min_length=20,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Question
        fields = ['title', 'content']
