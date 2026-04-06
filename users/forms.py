from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email Address')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'nationality', 'date_of_birth', 'bio', 'avatar']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
