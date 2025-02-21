from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db.models import fields
from .models import UserProfile
from .models import UserAnswer

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class AnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswer  # Ensure UserAnswer is defined elsewhere
        fields = ['answer']

