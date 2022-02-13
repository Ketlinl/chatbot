from django.contrib import admin
from .models import Capture


class CaptureAdmin(admin.ModelAdmin):
    """
    Gerenciamento de capturas.
    """

    fields = ('email', 'name', 'phone', 'document', 'age', 'sex', 'cep')

    list_display = ('email', 'name', 'phone', 'document', 'age', 'sex', 'cep')

    search_fields = ('email', 'name', 'phone', 'document')

    list_filter = ('sex', 'created_at')

    ordering = ('email', 'name')

    def save_model(self, request, obj, form, change):
        """
        Salva a modelo no banco de dados.
        """

        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        Modifica o comportamento da listagem
        """

        queryset = super().get_queryset(request)
        queryset = queryset.filter(user=request.user)
        return queryset

admin.site.register(Capture, CaptureAdmin)
