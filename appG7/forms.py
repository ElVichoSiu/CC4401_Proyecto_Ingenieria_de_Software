# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Sesion

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(max_length=500,
                          required=False,
                          widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    profile_pic = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']
        
class SesionFilterForm(forms.Form):
    ramo = forms.ChoiceField(choices=[('all', 'All')] + Sesion.Cursos, required=False)