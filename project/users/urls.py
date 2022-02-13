from django.contrib.auth import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='users:login'), name='logout'),
]
