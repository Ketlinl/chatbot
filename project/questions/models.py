from django.db import models
from project.users.models import User


class Question(models.Model):
    """
    Cadastra as perguntas e respostas
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name="questions"
    )

    input_before = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        verbose_name="Pergunta anterior",
        related_name="related_inputs",
        null=True, blank=True
    )

    is_active = models.BooleanField(
        "Está ativo?",
        help_text="Verifica se a questão está ativo no sistema.",
        default=True
    )

    body = models.CharField(
        "Entrada",
        help_text="Enunciado da entrada do usuário",
        max_length=500
    )

    answer = models.CharField(
        "Resposta",
        help_text="Resposta para essa questão",
        max_length=500
    )

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

        return self.body

    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"
        db_table = "questions"
        ordering = ('created_at',)
