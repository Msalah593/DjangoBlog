from rest_framework import routers
from .views import ArticleViewSet, UserViewSet
from django.urls import path, include, re_path
from rest_framework.authtoken import views


router = routers.DefaultRouter()
router.register(r'user', UserViewSet, 'users')
router.register(r'article', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^api-token-auth/', views.obtain_auth_token)
]
