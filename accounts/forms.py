from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class SellerForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('shop_name', 'phone', 'bio')

    def clean_shop_name(self):
        name = self.cleaned_data['shop_name'].strip()
        if not name:
            raise forms.ValidationError("Please give your shop a name.")
        return name