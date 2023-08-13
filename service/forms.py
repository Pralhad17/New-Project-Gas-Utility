from django import forms
from .models import ServiceRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


# User & Admin Registration Form

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# User & Admin Login Form

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus', None)
        self.fields['username'].label = 'Username'

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        UserModel = get_user_model()

        if username and password:
            if '@' in username:
                users = UserModel.objects.filter(email=username)
                if users.exists() and users.first().check_password(password):
                    self.user_cache = users.first()
                else:
                    raise forms.ValidationError("Invalid email or password")
            else:
                self.user_cache = authenticate(self.request, username=username, password=password)

            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password")

        self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


# Customer Service request Form

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['request_type', 'details', 'proof']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['request_type'].widget.attrs['class'] = 'form-select'
        self.fields['details'].widget.attrs['class'] = 'form-control'
        self.fields['proof'].widget.attrs['class'] = 'form-control'



