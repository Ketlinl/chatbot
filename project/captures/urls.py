from django.urls import path
from project.captures import views

urlpatterns = [
    path("<int:user_id>/", views.captures)
]
