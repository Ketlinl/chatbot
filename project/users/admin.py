from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from django.db.models import Q
from .forms import UserCreationForm, UserForm
from .models import User


class UserAdmin(BaseUserAdmin):
    """
    Configuração de formulário de usuário administrador.
    """

    form = UserForm

    fieldsets = ((None, {'fields': ('email', 'name', 'is_active')}),)

    add_form = UserCreationForm

    add_fieldsets = ((None, {'fields': ('email', 'name', 'password1', 'password2')}),)

    list_display = ('name', 'email', 'is_active', 'is_staff', 'created_at')

    search_fields = ('name', 'email')

    list_filter = ('created_at', 'is_active', 'is_staff')

    ordering = ('email', )

    actions = ('active_user', 'desactive_user')

    def get_ordering(self, request):
        """
        Reordena os itens
        """

        return ('-is_staff', 'name', '-created_at')

    def active_user(self, request, queryset):
        """
        Ativa um determinado usuário.
        """

        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} Usuários ativados com sucesso!")

    active_user.short_description = 'Ativar usuários'

    def desactive_user(self, request, queryset):
        """
        Desativa um determinado usuário.
        """

        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} Usuários desativados com sucesso!")

    desactive_user.short_description = 'Desativa usuários'


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
