from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser
import ast


def confirmation_view(request, *args, **kwargs):
    user = request.user
    return render(request, 'users/confirmation.html',
                  {'user': user, 'status': 'confirmation sent'})


def activate(request, usernameb, token):
    usernameb = ast.literal_eval(usernameb)
    username = urlsafe_base64_decode(usernameb).decode()
    user = get_object_or_404(CustomUser, username=username)
    token_is_valid = default_token_generator.check_token(user, token)
    if token_is_valid and not user.is_active:
        user.is_active = True
        user.save()
        return render(request, 'users/confirmation.html',
                      {'user': user, 'status': 'user activated'})
    else:
        return render(request, 'users/confirmation.html',
                      {'status': 'invalid token'})


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('confirmation')
    template_name = 'users/signup.html'
