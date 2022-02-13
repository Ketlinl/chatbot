from django.db import models
from project.users.models import User


class Question(models.Model):
    """
    Cadastra as perguntas e respostas
    """

    code = models.CharField(
        'Código',
        help_text="Código único de identificação da questão.",
        max_length=50,
        unique=True,
        error_messages={'unique': 'Código já existe.'}
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name="questions"
    )

    code_relation = models.CharField(
        "Código relacionado",
        help_text="Código usado para identificar respostas relacionadas",
        max_length=15
    )

    is_active = models.BooleanField(
        "Está ativo?",
        help_text="Verifica se a questão está ativo no sistema.",
        default=False
    )

    question = models.CharField(max_length=500)

    answer = models.CharField(max_length=500)

    created_at = models.DateTimeField(
        'Criado em',
        help_text="Data na qual a questão foi feita.",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Atualizado em',
        help_text="Data na qual a questão foi atualizada.",
        auto_now=True
    )

    def __str__(self):
        """
        Representação da modelo
        """

        return self.question

    class Meta:
        db_table = "questions"
        ordering = ('created_at',)
