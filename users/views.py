import secrets
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.core.mail import send_mail
from .models import CustomUser
from config import settings
from .forms import CustomUserCreationForm, CustomUserLoginForm


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        list_forbidden_words = settings.FORBIDDEN_WORDS
        context['forbidden_words'] = list_forbidden_words
        return context

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(32)
        user.token = token
        user.save()
        host = self.request.get_host()
        url_for_confirm = f'http://{host}/profile/email-confirm/{token}'
        send_mail(
            subject=f'Добро пожаловать в наш сервис. Подтвердите вашу электронную почту.',
            message=f'Здравствуйте {user.last_name} {user.first_name}! Для активации вашей учетной записи пройдите по '
                    f'ссылке {url_for_confirm} .',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

    def get_success_url(self):
        next = self.request.POST.get('next', '/')
        return next


class AuthorizationView(LoginView):
    form_class = CustomUserLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('catalog:home')

    def get_success_url(self):
        next = self.request.POST.get('next', '/')
        return next


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profile.html'
    context_object_name = 'profile'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'editing_profile.html'
    success_url = reverse_lazy('user:profile')


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.groups.add(Group.objects.get(name='Зарегистрированный пользователь'))
    user.save()
    subject = f'Добро пожаловать в наш сервис, {user.last_name} {user.first_name}.'
    message = f'Здравствуйте {user.last_name} {user.first_name}! Спасибо, что зарегистрировались в нашем сервисе!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
    return redirect(reverse('catalog:home'))
