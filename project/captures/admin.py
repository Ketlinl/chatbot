from django.contrib import admin
from .models import Capture
import re as regex
import buscacep


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

        if obj.zip_code:
            try:
                response = buscacep.busca_cep_correios(obj.zip_code)
            except:
                response = None

            print(response)
            if response:
                if not obj.state:
                    obj.state = response.localidade[response.localidade.index("/"):].replace("/", "").strip()

                if not obj.city:
                    obj.city = response.localidade[:response.localidade.index("/")].strip()

                if not obj.neighborhood:
                    obj.neighborhood = response.bairro.strip()

                if not obj.address:
                    obj.address = response.logradouro.strip()

                if not obj.number:
                    obj.number = regex.sub('[0-9/]', '', response.logradouro)

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        Modifica o comportamento da listagem
        """

        queryset = super().get_queryset(request)
        queryset = queryset.filter(user=request.user)
        return queryset

admin.site.register(Capture, CaptureAdmin)
