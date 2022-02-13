from django.contrib.auth.forms import UserCreationForm as CreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class UserForm(forms.ModelForm):
    """
    Cria um formulário para ser usado no django admin.
    """

    class Meta:
        model = User
        fields = ('email', 'name', 'is_active')


class UserCreationForm(CreationForm):
    """
    Cria um formulário para adicionar um novo usuário porém sem permissão
    para se autenticar no admin.
    """

    class Meta:
        model = User
        fields = ('name', 'email')
