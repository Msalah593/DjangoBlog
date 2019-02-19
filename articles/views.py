from django.shortcuts import render,reverse
from django.views import generic
from .models import Article
from django.urls import reverse_lazy

# Create your views here.

class ArticleList(generic.ListView):
    ordering=['-pub_date']
    model=Article
    template_name='index.html'
    context_object_name='articles'

class ArticleCreate(generic.CreateView):
    model=Article
    template_name='create_article.html'
    fields=['title','body']
    success_url=reverse_lazy('home')


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
