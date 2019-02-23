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
from users.views import login_view,SignUp,confirmation_view,activate
from articles.views import ArticleList,ArticleCreate,articledetials,UserArticleList,ArticleUpdate
from api.views import ArticleViewSet,CreateViewSet,SignupView
from rest_framework import routers, serializers, viewsets
# from django.conf.urls import url, include
# from users.models import CustomUser


# # Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('url', 'username', 'email', 'is_staff')

# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer

# # Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'article', ArticleViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('django.contrib.auth.urls')),
    path('',ArticleList.as_view(), name='home'),
    path('createarticle',ArticleCreate.as_view(),name='createarticle'),
    path('articles/<id>/', articledetials, name='article-detail'),
    path('articles/<pk>/update',ArticleUpdate.as_view() , name='article-update'),
    path('users/signup/', SignUp.as_view(),name='signup'),
    path('users/confirmation/', confirmation_view,name='confirmation'),
    path('users/articles/<user>',UserArticleList.as_view(),name='user-articles'),
    # re_path(r'users/validate/(?P<uidb64>[0-9A-Za-z_\-\']+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate,name='user-activation-link'),
    # url(r'^api/', include(router.urls)),
    # url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path('api/articles', ArticleViewSet.as_view({'get': 'list'})),
    path('api/articles/create', CreateViewSet.as_view({'post': 'create'})),
    path('api/signup',SignupView.as_view({'post':'create'}))
]
