from django.shortcuts import render
from .serializers import ArticleSerializer,SignupSerializer
from rest_framework import viewsets, permissions,authentication
from articles.models import Article

# Create your views here.

class CreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.BasicAuthentication]

    # def get_queryset(self):
    #     qs = self.queryset.filter(author=self.request.user)
    #     return qs
    serializer_class = ArticleSerializer
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

class SignupView(viewsets.ModelViewSet):
    serializer_class = SignupSerializer
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()