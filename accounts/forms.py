from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class RegisterForm(UserCreationForm):
    """Custom user registration form with email validation and modern UI styling."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'name@example.com',
            'autocomplete': 'email',
            'id': 'reg-email',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Choose a username',
            'autocomplete': 'username',
            'id': 'reg-username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Create strong passphrase',
            'autocomplete': 'new-password',
            'id': 'reg-password1',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Repeat passphrase',
            'autocomplete': 'new-password',
            'id': 'reg-password2',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email


class LoginForm(AuthenticationForm):
    """Custom authentication form with styled inputs."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username or Email',
            'autocomplete': 'username',
            'id': 'login-username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
            'id': 'login-password',
        })
    )
