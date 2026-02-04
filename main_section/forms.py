from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField
from django.core.validators import MinLengthValidator, MaxLengthValidator, ProhibitNullCharactersValidator


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=25,
        validators=[MinLengthValidator(2),
                    MaxLengthValidator(25),
                    ProhibitNullCharactersValidator(
                        message='Нулевые символы использовать нельзя'
                    )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя'
        })
    )
    password1 = forms.CharField(
        validators=[MinLengthValidator(11, message='Пароль не короче 11 символов'),
                    MaxLengthValidator(20, message='Пароль не длиннее 20 символов'),
            ProhibitNullCharactersValidator(
            message='Нулевые символы использовать нельзя'
        )],
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        }),
        # help_text="Пароль должен содержать не менее 8 символов"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля'
        })
    )
    captcha = CaptchaField(
        validators=[ProhibitNullCharactersValidator(
            message='Нулевые символы использовать нельзя'
        )],
        label='Введите код с картинки',
        error_messages={'invalid': 'Неправильный код с картинки'}
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'captcha']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['captcha'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': 'Введите код с картинки'
        })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Это имя пользователя уже занято")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 != password1:
            raise ValidationError("Пароли не совпадают")




class LoginFormWithCaptcha(AuthenticationForm):
    captcha = CaptchaField(
        validators=[ProhibitNullCharactersValidator(
            message='Нулевые символы использовать нельзя'
        )],
        label='Введите код с картинки',
        error_messages={'invalid': 'Неправильный код с картинки'}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].validators.append(
            ProhibitNullCharactersValidator(
                message='Нулевые символы использовать нельзя'
            )
        )

        self.fields['password'].validators.append(
            ProhibitNullCharactersValidator(
                message='Нулевые символы использовать нельзя'
            )
        )

        # Настраиваем виджеты полей
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': 'Имя пользователя'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': 'Пароль'
        })
        self.fields['captcha'].widget.attrs.update({
            'class': 'form-control',
            # 'placeholder': 'Введите код с картинки'
        })