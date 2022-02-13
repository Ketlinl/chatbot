from django.shortcuts import render


def home(request):
    """
    View de capturas de dados.
    """

    return render(request, template_name="home.html")
