from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('chatbot/<str:protocol>/', views.chatbot),
    path('questao/<str:protocol>/answer/<int:input_before_id>/<str:current_input>/', views.nlk_process)
]
