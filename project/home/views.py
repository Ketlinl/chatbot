from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
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
            "protocol": "TJY8YP"
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
