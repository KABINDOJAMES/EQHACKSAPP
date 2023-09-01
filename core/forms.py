from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'enter email'}))
    
    first_name = forms.CharField(max_length=50, required = True, help_text ='required', 
              widget=forms.TextInput(attrs={'placeholder': 'first name'}))
    
    
    last_name = forms.CharField(max_length=50, required = False, help_text ='optional', 
              widget=forms.TextInput(attrs={'placeholder': 'last name'})
             )

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        
        help_texts = {
            'username': None,
            'email': None,
            'password2': None,
        }
        
        widgets = {
            'username': forms.TextInput(attrs={
                        'placeholder':'Username',
                }),  

        }


class NewTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('location', 'contact_number', 'affected_person_contact', 'title', 'description')

class DonateForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ('location', 'contact_number', 'amount_donated')
