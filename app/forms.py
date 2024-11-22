from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from app.models import UserProfile, Question, Tag, Answer


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, label=_('Username'))
    password = forms.CharField(min_length=6, widget=forms.PasswordInput, label=_('Password'))


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(),
        min_length=6
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(),
    )
    username = forms.CharField(
        label=_('Username')
    )
    email = forms.CharField(
        label=_('Email address')
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
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             label=_('Email address'))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                              label=_('Avatar'))

    class Meta:
        model = User
        fields = ['email', 'avatar']

    def save(self, **kwargs):
        user = super().save(**kwargs)

        profile = user.userprofile
        received_avatar = self.cleaned_data.get('avatar')
        if received_avatar:
            profile.avatar = self.cleaned_data.get('avatar')
            profile.save()

        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_('Old Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}),
    )
    new_password1 = forms.CharField(
        label=_('New Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
    )
    new_password2 = forms.CharField(
        label=_('Confirm New Password'),
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
        label=_("Enter tags (', '-separated)"),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    title = forms.CharField(
        label=_("Title"),
        strip=True,
        required=True,
        min_length=10
    )

    content = forms.CharField(
        label=_("Describe your question"),
        strip=True,
        required=True,
        min_length=20,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Question
        fields = ['title', 'content']


class AnswerForm(forms.ModelForm):
    content = forms.CharField(
        label=_("Put your answer here"),
        strip=True,
        required=True,
        min_length=20,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Answer
        fields = ['content']
