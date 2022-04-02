import email
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import JsonResponse
from project.users.forms import UserCreationForm
from ..pln import PLN
import nltk
import os

User = get_user_model()


def home(request):
    """
    View de capturas de dados.
    """

    env = os.environ.get("ENVIRONMENT", "development")

    if env == "development":
        host = "localhost:8000"
    else:
        host = "chatbot.vwapp.com.br"

    user = User.objects.filter(is_superuser=True, is_staff=True).last()

    return render(
        request,
        template_name="home.html",
        context={
            "host": host,
            "protocol": user.chatbot.protocol if user else ""
        }
    )


def chatbot(request, protocol):
    """
    Abre a página do chatbot.
    """

    nltk.download("stopwords")
    nltk.download("rslp")

    return render(
        request,
        template_name="chatbot.html",
        context={"protocol": protocol}
    )


def nlk_process(request, protocol, input_before_id, current_input):
    """
    Realiza o processamento de linguagem natural extraindo as
    informações importantes.
    """

    result = PLN(protocol, input_before_id, current_input).get_result()
    return JsonResponse(result, safe=False)


def create_ong(request):
    """
    Mostra o formulário de criação da ONG.
    """

    form = UserCreationForm(request.POST, None)

    group = Group.objects.last()

    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['email'],
            data['name'],
            data['password1']
        )
        user.groups.add(group)

        return HttpResponseRedirect('/admin/')

    return render(request, 'form.html', {"form": form})
