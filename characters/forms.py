from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Note, NOTE_MAX_LENGTH


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'maxlength': NOTE_MAX_LENGTH,
                'placeholder': 'Ваша заметка о персонаже...',
            }),
        }
        labels = {'text': ''}
