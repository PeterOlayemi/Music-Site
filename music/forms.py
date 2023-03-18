from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['email', 'content']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
