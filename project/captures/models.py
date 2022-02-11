from django.db import models
from project.users.models import User


class Capture(models.Model):
    """
    Classe responsável por capturar as informações que o usuário
    digitar no chatbot.
    """

    code = models.CharField(
        'Código',
        help_text="Código único de identificação da captura.",
        max_length=50,
        unique=True,
        error_messages={'unique': 'Código já existe.'}
    )

    email = models.EmailField(
        "Email",
        help_text="Email único do usuário capturado.",
        max_length=50,
        unique=True,
        error_messages={'unique': 'Email já existe na base de dados.'}
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name="captures"
    )

    name = models.CharField(
        "Nome",
        help_text="Nome do usuário capturado.",
        max_length=50
    )

    phone = models.CharField(
        "Telefone",
        help_text="Telefone capturado do usuário.",
        max_length=15
    )

    document = models.CharField(
        "CPF/CNPJ",
        help_text="Documento capturado do usuário, pode ser CPF ou CNPJ.",
        max_length=25
    )

    age = models.IntegerField(
        "Idade",
        help_text="Idade capturada do usuário.",
        null=True
    )

    sex = models.CharField(
        "Sexo",
        help_text="Captura o sexo de uma pessoa. Ex: M ou F",
        choices=(("M", "Masculino"), ("F", "Feminino")),
        max_length=1,
        blank=True
    )

    cep = models.CharField(
        "CEP",
        help_text="Captura do CEP do usuário",
        max_length=10
    )

    state = models.CharField(
        "Estado",
        help_text="Estado capturado do usuário.",
        max_length=50,
        blank=True
    )

    city = models.CharField(
        "Cidade",
        help_text="Cidade capturada do usuário",
        max_length=100,
        blank=True
    )

    neighborhood = models.CharField(
        "Bairro",
        help_text="Bairro capturado do usuário.",
        max_length=100,
        blank=True
    )

    address = models.CharField(
        "Endereço",
        help_text="Endereço capturado do usuário.",
        max_length=255,
        blank=True
    )

    number = models.CharField(
        "Número",
        help_text="Captura do número do endereço.",
        max_length=5,
        blank=True
    )

    is_active = models.BooleanField(
        "Está ativo?",
        help_text="Verifica se o usuário capturado está ativo no sistema.",
        default=False
    )

    created_at = models.DateTimeField(
        'Criado em',
        help_text="Data na qual a captura foi feita.",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Atualizado em',
        help_text="Data na qual a captura foi atualizada.",
        auto_now=True
    )

    def __str__(self):
        """
        Representação da modelo
        """

        return self.code

    class Meta:
        db_table = "captures"
        ordering = ('created_at',)
