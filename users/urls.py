from .apps import UsersConfig
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegisterView, email_verification, ProfileView, ProfileUpdateView, AuthorizationView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', AuthorizationView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/editing_profile/', ProfileUpdateView.as_view(), name='editing_profile'),
]

handler404 = "catalog.views.page_not_found_view"
