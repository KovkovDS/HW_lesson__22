from .apps import UsersConfig
from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import RegisterView, UserLoginView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
]
