"""DjangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from users.views import SignUp,confirmation_view,activate
from articles.views import ArticleList,ArticleCreate,articledetials,UserArticleList,ArticleUpdate
from api.views import ArticleViewSet,UserViewSet
from rest_framework import routers, serializers, viewsets

router = routers.DefaultRouter()
router.register(r'article', ArticleViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('django.contrib.auth.urls')),
    re_path(r'^api/', include(router.urls)),
    path('',ArticleList.as_view(), name='home'),
    path('createarticle',ArticleCreate.as_view(),name='createarticle'),
    path('articles/<id>/', articledetials, name='article-detail'),
    path('articles/<pk>/update',ArticleUpdate.as_view() , name='article-update'),
    path('users/signup/', SignUp.as_view(),name='signup'),
    path('users/confirmation/', confirmation_view,name='confirmation'),
    path('users/articles/<user>',UserArticleList.as_view(),name='user-articles'),
    re_path(r'users/validate/(?P<uidb64>[0-9A-Za-z_\-\']+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate,name='user-activation-link'),
]
