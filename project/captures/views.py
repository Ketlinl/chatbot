from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from .models import Capture

User = get_user_model()


class CapturesView(LoginRequiredMixin, TemplateView):
    """
    Listagem de questões
    """

    model = User
    template_name = 'captures.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """
        Insere novos contextos no template.
        """

        context = super(CapturesView, self).get_context_data(**kwargs)
        context['captures'] = Capture.objects.filter(user=self.request.user)
        return context
