from django.shortcuts import render,reverse
from django.views import generic
from .models import Article
from django.urls import reverse_lazy
from django.utils import six
from django.db.models import Q

# Create your views here.

class ArticleList(generic.ListView):
    ordering=['-pub_date']
    model=Article
    template_name='index.html'
    context_object_name='articles'

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        query = self.request.GET.get('q')
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        if query:
            queryset = queryset.filter(Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(author__email__icontains=query) | 
                Q(author__username__icontains=query))
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class ArticleCreate(generic.CreateView):
    model=Article
    template_name='create_article.html'
    fields=['title','body']
    success_url=reverse_lazy('home')


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
