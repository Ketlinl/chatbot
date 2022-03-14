from django.contrib import admin
from .models import Question
from .forms import QuestionForm


class QuestionAdmin(admin.ModelAdmin):
    """
    Gerenciador de questões na administração.
    """

    form = QuestionForm

    fields = ('input_before', 'body', 'answer', 'is_active')

    list_display = ('body', 'answer', 'input_before', 'is_active', 'id')

    search_fields = ('id', 'body', 'answer')

    list_filter = ('is_active', 'created_at', 'input_before')

    ordering = ('body',)

    def save_model(self, request, obj, form, change):
        """
        Salva a modelo no banco de dados.
        """

        obj.chatbot = request.user.chatbot
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        Modifica o comportamento da listagem
        """

        queryset = super().get_queryset(request)
        queryset = queryset.filter(chatbot__user=request.user)
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filtrar somente as questões do usuário.
        """

        if db_field.name == 'input_before':
            queryset = kwargs.get('queryset', db_field.remote_field.model.objects)
            kwargs['queryset'] = queryset.filter(chatbot__user=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Question, QuestionAdmin)
