from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordChangeForm
from .models import CustomUser


class CustomUserCreation(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password', 'password2', 'email')


class CustomUserChange(UserChangeForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    date_joined = forms.CharField(max_length=100)

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'password', 'email')


class PasswordUserChange(PasswordChangeForm):
    old_password = forms.CharField(max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'passowrd'}))
    new_password1 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'passowrd'}))
    new_password2 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'passowrd'}))

    class Meta(PasswordChangeForm):
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')
