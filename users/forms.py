from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text=None
        self.fields['password1'].help_text=None
        self.fields['password2'].help_text=None
        self.fields['username'].label=""
        self.fields['password1'].label=""
        self.fields['password2'].label=""

        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Lietotājvārds'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Parole'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': 'Paroles apstiprinājums'})