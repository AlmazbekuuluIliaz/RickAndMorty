from django import forms

from .models import Note, NOTE_MAX_LENGTH


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
