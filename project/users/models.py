from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class UserProfileManager(BaseUserManager):
    """
    Classe responsável por sobrescrever o objects padrão do user.
    """

    def create_user(self, email, name, password=None):
        """
        Cria um novo usuário comum.
        """

        if not email:
            raise ValueError("Usuário deve ter um endereço de email.")

        email = self.normalize_email(email)

        user = self.model(email=email, name=name)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """
        Cria um usuário com permissões de administração.
        """

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Cria um usuário de autenticação no sistema.
    """

    email = models.EmailField(
        'E-mail',
        help_text="Email que será usado como nome de usuário.",
        unique=True,
        error_messages={'unique': "Usuário com esse email já existe."}
    )

    name = models.CharField(
        'Nome',
        help_text="Nome Completo",
        max_length=150
    )

    is_active = models.BooleanField(
        'Está Ativo?',
        help_text="Verifica se o usuário está ativo no sistema.",
        default=True
    )

    is_staff = models.BooleanField(
        'É administrador?',
        help_text="Verifica se o usuário é um administrador.",
        default=False
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

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """
        Retorna o objeto formatado
        """

        return self.email

    class Meta:
        """
        Mais informações
        """

        db_table = "users"
        ordering = ('email',)
