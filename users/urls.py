from .apps import UsersConfig
from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import RegisterView, email_verification, ProfileView, ProfileUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html', next_page='catalog:home'), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/editing_profile/', ProfileUpdateView.as_view(), name='editing_profile'),
]
