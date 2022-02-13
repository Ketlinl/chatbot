from django.shortcuts import render
from .models import Capture


def captures(request, user_id):
    """
    View de capturas de dados.
    """

    captures = Capture.objects.filter(user__id=user_id)

    return render(
        request,
        template_name="captures.html",
        context={
            "user_id": user_id,
            "captures": captures
        }
    )
