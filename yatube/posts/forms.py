from django import forms
from django.forms import TextInput, Textarea, Select

from .models import *


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].empty_label = "Категория не выбрана"
        self.fields['text'].label = 'Содержание'
        self.fields['group'].label = 'Группа'

    class Meta:
        model = Post
        fields = ['text', 'group']






