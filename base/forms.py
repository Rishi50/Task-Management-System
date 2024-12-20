from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import tasklist

from .models import Profile

# Reordering Form and View
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class PositionForm(forms.Form):
    position = forms.CharField()

class todo_task(ModelForm):
    class Meta:
        model = tasklist
        fields = ['title','memo','important']

class CustomUserCreationForm(UserCreationForm):
    # Add custom fields or modify existing fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    email = forms.EmailField(
        required=True,
        
    )

    class Meta:
        model = User

        

        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': None,
            'email': None,
            'password1' : None,
            'password2' : None,
        }

        
    # Custom validation for the email field
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    # Optional: Add custom validation for the password field
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password
