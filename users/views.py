from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegisterForm
from .models import User

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()

        # Отправка приветственного письма
        send_mail(
            subject="Добро пожаловать в TechZone!",
            message=f"Здравствуйте, {user.username}!\n\nСпасибо за регистрацию в нашем интернет-магазине TechZone. "
                    f"Теперь вы можете добавлять товары в корзину, оставлять отзывы и следить за новинками.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        login(self.request, user)
        messages.success(self.request, f"Добро пожаловать, {user.username}! Вы успешно зарегистрированы.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)
