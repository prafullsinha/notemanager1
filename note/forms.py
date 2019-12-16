from django import forms
from .models import NoteModel, CommentModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NoteModelForm(forms.ModelForm):
    categories = forms.CharField(label="Category")

    class Meta:
        model = NoteModel
        fields = ('title', 'description', 'categories')


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Name")

    class Meta:
        model = User
        fields = ('email', 'first_name')


class CommentModelForm(forms.ModelForm):
    comment = forms.CharField(label="")

    class Meta:
        model = CommentModel
        fields = ('comment',)



