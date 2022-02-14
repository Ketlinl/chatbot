from django.contrib import admin
from .models import Capture
from ..utils import zip_code_request
import re as regex


class CaptureAdmin(admin.ModelAdmin):
    """
    Gerenciamento de capturas.
    """

    fieldsets = (
        (None, {'fields': ('email', 'name', 'phone', 'document', 'age', 'sex')}),
        ('ENDEREÇO', {
            'fields': ('zip_code', 'state', 'city', 'neighborhood', 'address', 'number'),
            'classes': ('extrapretty', 'collapse', 'in')
        })
    )

    list_display = ('email', 'name', 'phone', 'document', 'age', 'sex', 'zip_code')

    search_fields = ('email', 'name', 'phone', 'document')

    list_filter = ('sex', 'created_at')

    ordering = ('email', 'name')

    def save_model(self, request, obj, form, change):
        """
        Salva a modelo no banco de dados.
        """

        obj.user = request.user

        address = zip_code_request(obj.zip_code)

        if address:
            if not obj.state:
                obj.state = address['state']

            if not obj.city:
                obj.city = address['city']

            if not obj.neighborhood:
                obj.neighborhood = address['neighborhood']

            if not obj.address:
                obj.address = address['address']

            if not obj.complement:
                obj.complement = address['complement']

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        Modifica o comportamento da listagem
        """

        queryset = super().get_queryset(request)
        queryset = queryset.filter(user=request.user)
        return queryset

admin.site.register(Capture, CaptureAdmin)
