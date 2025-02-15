from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from config import settings
from .models import CustomUser
from django_countries.widgets import CountrySelectWidget


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'avatar', 'first_name', 'last_name', 'phone_number', 'country', 'password1', 'password2')
        widgets = {"country": CountrySelectWidget(layout='{widget}<img class="country-select-flag" id="{flag_id}" '
                                                         'style="margin: 3px 4px 6px; width: 2.5%; height: 2.5%" '
                                                         'src="{country.flag}">')}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise forms.ValidationError('Некорректный адрес электронной почты. Пожалуйста введите корректные данные.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр.')
        return phone_number

    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get('email')
    #     first_name = cleaned_data.get('first_name')
    #     last_name = cleaned_data.get('last_name')
    #
    #     for forbidden_word in settings.FORBIDDEN_WORDS:
    #         if forbidden_word.lower() in email.lower() or first_name.lower() or last_name.lower():
    #             raise ValidationError('Вы использовали какие-то слова из списка запрещенных слов. '
    #                                   'Ознакомьтесь с данным списком и введите описание товара, не использую слова из '
    #                                   'него.')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите ваш E-mail'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control', 'type': 'file', 'id': 'formFile',
                                                   'label': 'Фото профиля'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите ваше имя'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите вашу фамилию'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control',
                                                         'placeholder': 'Введите ваш номер телефона',
                                                         'label': 'Номер телефона'})


class CustomUserLoginForm(AuthenticationForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
