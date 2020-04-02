from django import forms
from .models import Signup, Account
from projects.models import Profile
from django.contrib.auth.forms import UserCreationForm

class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "name": "email",
        "id": "email",
        "placeholder": "e-mail kamu",
    }), label="")

    class Meta:
        model = Signup
        fields = ('email', )

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2',]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ['username', 'email',]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

