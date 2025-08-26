from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    phone_number = forms.CharField(max_length=17, required=False, label="Номер телефона")
    country = forms.CharField(max_length=50, required=False, label="Страна")
    avatar = forms.ImageField(required=False, label="Аватар")

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'country', 'avatar', 'password1', 'password2')
