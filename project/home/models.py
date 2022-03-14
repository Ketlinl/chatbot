from django.db import models


class Chatbot(models.Model):
    """
    Modelo de chatbot
    """

    protocol = models.CharField(
        "protocolo",
        help_text="Protocolo do chatbot do usuário",
        unique=True,
        error_messages={'unique': "Protocolo já existe."},
        max_length=25
    )

    is_active = models.BooleanField(
        "Está ativo?",
        help_text="Verifica se a questão está ativo no sistema.",
        default=True
    )

    created_at = models.DateTimeField(
        'Criado em',
        help_text="Data na qual o usuário foi criado.",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Atualizado em',
        help_text="Data na qual o usuário foi atualizado.",
        auto_now=True
    )

    def __str__(self):
        """
        Representação da modelo
        """

        return self.protocol

    class Meta:
        verbose_name = "Chatbot"
        verbose_name_plural = "Chatbot"
        db_table = "chatbot"
        ordering = ('created_at',)
