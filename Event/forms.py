from django import forms
from .models import Participant

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']
        labels = {
            'name': 'NAME',
            'email': 'EMAIL',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        }
