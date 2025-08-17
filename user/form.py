from django.forms import ModelForm
from base.models import User
from django.contrib.auth.forms import UserCreationForm


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'bio']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']
