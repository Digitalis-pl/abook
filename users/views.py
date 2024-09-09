from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import (PasswordResetConfirmView, PasswordResetDoneView,
                                       PasswordResetCompleteView, PasswordResetView)
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from users.models import User
from users.forms import UserRegistrationForm
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER

import secrets

from users.services import make_random_password


# Create your views here.


class CreateUser(CreateView):
    model = User
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/confirm-email/{token}/'
        send_mail(subject='Подтверждение пароля',
                  message=f'Для подтверждения перейдите по ссылке {url}',
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[user.email])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('newsletter_app:main_page')


class UserListView(PermissionRequiredMixin, ListView):
    permission_required = 'users.view_user'
    model = User


class ChangeUserView(UpdateView):
    model = User
    fields = ('email', 'first_name', 'last_name', 'phone')

    def get_success_url(self):
        return reverse('users:account_change', kwargs={'pk': self.object.pk})


class DeleteUserView(DeleteView):
    model = User
    success_url = reverse_lazy('newsletter_app:main_page')


class PasswordReset(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')

    def form_valid(self, form):
        if self.request.method == 'POST':
            user_email = self.request.POST.get('email')
            user = User.objects.filter(email=user_email).first()
            if user:
                new_password = make_random_password()
                user.set_password(new_password)
                user.save()
                try:
                    send_mail(
                        subject="Восстановление пароля",
                        message=f"Здравствуйте! Ваш пароль для доступа на наш сайт изменен:\n"
                                f"Данные для входа:\n"
                                f"Email: {user_email}\n"
                                f"Пароль: {new_password}",
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[user.email]
                    )
                except Exception:
                    print(f'Ошибка пр отправке письма, {user.email}')
                return HttpResponseRedirect(reverse('users:password_reset_done'))


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password-confirm')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class ResetComplete(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    if user:
        user.is_active = True
        user.save()
    else:
        return redirect(reverse('users:error_page'))
    return redirect(reverse('users:login'))


def user_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse('users:users'))
