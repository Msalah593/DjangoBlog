from .serializers import ArticleSerializer, SignupSerializer
from rest_framework import viewsets
from articles.models import Article
from django.contrib.auth.hashers import make_password

from users.models import CustomUser
# Create your views here.
from .permissions import Usercreation, Articlecreation
from rest_framework import filters


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ('title',)

        elif request.query_params.get('body_only'):
            return ('body',)
        return super(CustomSearchFilter, self).get_search_fields(view, request)


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [Articlecreation]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (CustomSearchFilter, filters.OrderingFilter)
    ordering_fields = ('author', 'title', 'body', 'pub_date')
    search_fields = ('title', 'body')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = SignupSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (Usercreation,)

    def perform_create(self, serializer):
        serializer.validated_data['password'] = make_password(
            serializer.validated_data['password'])
        serializer.save()
