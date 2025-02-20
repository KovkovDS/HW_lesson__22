import secrets
from urllib.parse import urlparse
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse, is_valid_path
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.core.mail import send_mail
from .models import CustomUser
from config import settings
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth.views import LoginView


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        url_for_confirm = f'http://{host}/profile/email-confirm/{token}/'
        send_mail(
            subject=f'Добро пожаловать в наш сервис. Подтвердите вашу электронную почту.',
            message=f'Здравствуйте {user.last_name} {user.first_name}! Для активации вашей учетной записи пройдите по '
                    f'ссылке {url_for_confirm} .',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomUserLoginForm
    success_url = reverse_lazy('catalog:home')

    # def get_success_url(self, **kwargs):
    #     next_url = self.request.GET.get('next', '/')
    #     if '/profile/email-confirm/' in next_url:
    #         return redirect(reverse('catalog:home'))
    #     if self.request.method == 'POST':
    #         form = AuthenticationForm(data=self.request.POST)
    #         if form.is_valid():
    #             user = form.get_user()
    #             login(self.request, user)
    #             next_url = self.request.POST.get('next', next_url)
    #             parsed_url = urlparse(next_url)
    #             if not parsed_url.netloc and is_valid_path(next_url):
    #                 return next_url
    #             return HttpResponseRedirect('/')
    #     else:
    #         form = AuthenticationForm()
    #
    #     return render(self.request, 'login.html', {'form': form, 'next': next_url})


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_success_url(self, **kwargs):
        next = self.request.POST.get('next', '/')
        return next


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'editing_profile.html'
    success_url = reverse_lazy('user:profile')


def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    subject = f'Добро пожаловать в наш сервис, {user.last_name} {user.first_name}.'
    message = f'Здравствуйте {user.last_name} {user.first_name}! Спасибо, что зарегистрировались в нашем сервисе!'
    from_email = 'dmitriy.vavtotrans@ya.ru'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
    return redirect(reverse('user:login'))
