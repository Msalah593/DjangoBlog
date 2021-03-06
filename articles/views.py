from django.shortcuts import render, get_object_or_404, Http404
from django.views import generic
from django.views.generic.edit import BaseUpdateView
from .models import Article
from django.urls import reverse_lazy
from django.utils import six
from django.db.models import Q
from .forms import ArticleForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.core.exceptions import ImproperlyConfigured


class ArticleList(generic.ListView):
    ordering = ['-pub_date']
    model = Article
    template_name = 'index.html'
    context_object_name = 'articles'

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


@method_decorator(login_required, name='dispatch')
class ArticleCreate(generic.CreateView):
    model = Article
    template_name = 'articles/create_article.html'
    fields = ['title', 'body']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ArticleUpdate(generic.UpdateView):
    model = Article
    fields = ['title', 'body']
    form = ArticleForm
    template_name = 'articles/updatearticle.html'
    success_url = reverse_lazy('home')

    def get(self, request, pk, *args, **kwargs):
        self.object = get_object_or_404(Article, id=pk)
        return super(BaseUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author.id == request.user.id:
            return super(BaseUpdateView, self).post(request, *args, **kwargs)
        else:
            return render(request, self.template_name, {})


def articledetials(request, id, *args, **kwargs):
    context = {}
    if id:
        obj = get_object_or_404(Article, id=id)
        context = {'article': obj}
    return render(request, 'articles/details.html', context)


class UserArticleList(generic.ListView):
    ordering = ['-pub_date']
    model = Article
    template_name = 'articles/userarticles.html'
    context_object_name = 'articles'

    def get(self, request, user, *args, **kwargs):
        if request.user.is_authenticated:
            self.object_list = Article.objects.filter(author=request.user)
            allow_empty = self.get_allow_empty()

            if not allow_empty:
                # When pagination is enabled and object_list is a queryset,
                # it's better to do a cheap query than to load the unpaginated
                # queryset in memory.
                if (self.get_paginate_by(self.object_list) is not None
                        and hasattr(self.object_list, 'exists')):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = len(self.object_list) == 0
                if is_empty:
                    raise Http404(('''Empty list and ''' +
                                   '''"%(class_name)s.allow_empty" is False.''')
                                  % {'class_name': self.__class__.__name__})
            context = self.get_context_data()
            return self.render_to_response(context)
        else:
            self.object_list = None
            context = self.get_context_data()
            return self.render_to_response({'owner': user})
