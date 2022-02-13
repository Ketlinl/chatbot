from django.contrib.auth import get_user_model
from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    """
    Cria um formulário para ser usado no django admin.
    """

    body = forms.CharField(
        label="Questão",
        required=True,
        help_text="Corpo da questão",
        error_messages={'required': "O corpo da questão é obrigatório."},
        widget=forms.Textarea(attrs={'rows': 10, 'cols': '100%'})
    )

    answer = forms.CharField(
        label="Resposta",
        required=True,
        help_text="Resposta da questão",
        error_messages={'required': "A resposta da questão é obrigatória."},
        widget=forms.Textarea(attrs={'rows': 10, 'cols': '100%'})
    )

    class Meta:
        model = Question
        fields = ('body', 'answer', 'is_active')
