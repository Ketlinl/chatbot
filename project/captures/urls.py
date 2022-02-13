from django.urls import path
from project.captures import views

app_name = 'captures'

urlpatterns = [
    path("", views.CapturesView.as_view(), name="list")
]
