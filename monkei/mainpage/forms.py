from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from .models import Post


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(label='Username or Email', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }))


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class PostForm(forms.ModelForm):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'file')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form_control'}),
            'content': forms.Textarea(attrs={'class': 'form_control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form_control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form_control'}),

        }

        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)
