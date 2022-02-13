from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin, UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from django.db.models import Q
from .forms import UserCreationForm, UserForm
from .models import User


class GroupAdmin(BaseGroupAdmin):
    """
    Sobrescrever as permissões removendo as não usadas.
    """

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """
        Formata os campos de many to many das permissões.
        """

        if db_field.name == 'permissions':
            queryset = kwargs.get('queryset', db_field.remote_field.model.objects)
            kwargs['queryset'] = queryset.filter(
                ~Q(content_type__app_label__in=[
                    "admin", "auth", "contenttypes", "sessions"
                ])
            )

        return super().formfield_for_manytomany(db_field, request=request, **kwargs)


class UserAdmin(BaseUserAdmin):
    """
    Configuração de formulário de usuário administrador.
    """

    form = UserForm

    fieldsets = ((None, {'fields': ('email', 'name', 'is_active')}),)

    add_form = UserCreationForm

    add_fieldsets = ((None, {'fields': ('email', 'name', 'password1', 'password2')}),)

    list_display = ('name', 'email', 'is_active', 'is_staff', 'is_superuser', 'created_at')

    search_fields = ('name', 'email')

    list_filter = ('created_at', 'is_active', 'is_staff', 'is_superuser')

    ordering = ('email', )

    actions = ('active_user', 'desactive_user')

    def get_fieldsets(self, request, obj=None):
        """
        Super usuários podem modificar permissões.
        """

        if not obj:
            return self.add_fieldsets

        fieldsets = super().get_fieldsets(request, obj)

        if request.user.is_superuser:
            fieldsets = (
                (None, {'fields': ('email', 'name')}),
                ('PERMISSÕES', {
                    'fields': ('is_active', 'is_staff', 'groups'),
                    'description': 'Sistema de permissões do usuário.',
                    'classes': ('extrapretty', 'collapse', 'in')
                })
            )

        return fieldsets

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

    def get_queryset(self, request):
        """
        Modifica o comportamento da listagem
        """

        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset

        queryset = queryset.filter(email=request.user.email)
        return queryset


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.site_header = "Chatbot Theo"
admin.site.site_title = "Parte Administrativa"
admin.site.index_title = "Bem vindo a parte administrativa do chatbot Theo"
admin.site.site_url = '/login/'
