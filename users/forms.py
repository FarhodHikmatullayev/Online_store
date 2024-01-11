from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .models import User


class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({
            "class": "form-control",
            "id": "id_username",
            "placeholder": "username...",
            "name": "username",
            "type": "text",
        })
        self.fields['password'].widget.attrs.update({
            "class": "form-control",
            "id": "id_password",
            "placeholder": "password...",
            "name": "password",
            "type": "password",
        })


class CreateUserForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            "placeholder": "username...",
            "class": 'form-control',
        })
        self.fields['phone'].widget.attrs.update({
            "class": 'form-control',
            "placeholder": "+998900000000"
        })
        self.fields['password1'].widget.attrs.update({
            "placeholder": 'password..',
            "class": 'form-control',
        })
        self.fields['password2'].widget.attrs.update({
            "placeholder": 'password..',
            "class": 'form-control',
        })

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_('Password don\'t match'))
            return password2
        raise forms.ValidationError(_('You should write passwords'))

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data.get('password1'))
        user.save()
        return user


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'photo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            "placeholder": "username...",
            "class": 'form-control',
        })
        self.fields['first_name'].widget.attrs.update({
            "placeholder": "first_name...",
            "class": 'form-control',
        })
        self.fields['last_name'].widget.attrs.update({
            "placeholder": "last_name...",
            "class": 'form-control',
        })
        self.fields['phone'].widget.attrs.update({
            "placeholder": 'phone',
            "class": 'form-control',
        })
        self.fields['photo'].widget.attrs.update({
            "class": 'form-control',
        })


class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_('Password don\'t match'))
            return password2
        raise forms.ValidationError(_('You should write passwords'))

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data['password1'])
        if commit:
            account.save()
        return account


class AccountChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')

    def __init__(self, *args, **kwargs):
        super(AccountChangeForm, self).__init__(*args, **kwargs)
        self.fields['password'].help_text = '<a href="%s">change password</a>.' % reverse_lazy(
            'admin:auth_user_password_change', args=[self.instance.id])

    def clean_password(self):
        return self.initial['password']
