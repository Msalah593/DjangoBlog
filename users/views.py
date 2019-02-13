from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import generic      
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser
# Create your views here.

def login_view(request, *args, **kwargs):
    return render(request,'index.html',{})

def confirmation_view(request, *args, **kwargs):
    user=request.user
    print("there is requires")
    return render(request,'confirmation.html',{user : 'user'})

def activate(request,uidb64,token):
    username = urlsafe_base64_decode(uidb64).decode("utf-8") 
    user = CustomUser.objects.get(username= username)
    token_is_valid=default_token_generator.check_token(user,token)
    if token_is_valid and not user.is_active:
        user.is_active=True
        user.save()
        return HttpResponse("User Activated !")
    else:
        return HttpResponse("invalid Token")

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('confirmation')
    template_name = 'signup.html'
