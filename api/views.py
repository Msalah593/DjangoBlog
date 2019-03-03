from django.shortcuts import render
from .serializers import ArticleSerializer,SignupSerializer
from rest_framework import viewsets, permissions,authentication
from articles.models import Article
from django.contrib.auth.hashers import check_password, make_password
from users.forms import CustomUserCreationForm
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from users.models import CustomUser
# Create your views here.
from .permissions import Usercreation,Articlecreation

class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [Articlecreation]
    # authentication_classes = [authentication.BasicAuthentication]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = SignupSerializer
    queryset=CustomUser.objects.all()
    permission_classes=(Usercreation,)
    def perform_create(self, serializer):
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()
    # @action(detail=False, methods=['post'])
    # def register(self, request):
    #     permission_classes=(permissions.IsAuthenticated,)
    #     from rest_framework.response import Response
    #     return Response(request.data,status=200)
    
