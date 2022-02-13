from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from project.questions.models import Question

User = get_user_model()


class QuestionsView(LoginRequiredMixin, TemplateView):
    """
    Listagem de questões
    """

    model = User
    template_name = 'questions.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """
        Insere novos contextos no template.
        """

        context = super(QuestionsView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(user=self.request.user)
        return context
