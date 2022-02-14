from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('chatbot/<str:protocol>/', views.chatbot),
    path('questao/<str:protocol>/answer/<int:code_before>/<str:question>/', views.nlk_process)
]
