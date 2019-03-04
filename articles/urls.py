from django.urls import path
from .views import (ArticleCreate, articledetials,
                    UserArticleList, ArticleUpdate)


urlpatterns = [
    path('createarticle', ArticleCreate.as_view(), name='createarticle'),
    path('<id>/', articledetials, name='article-detail'),
    path('<pk>/update', ArticleUpdate.as_view(),
         name='article-update'),
    path('<user>', UserArticleList.as_view(),
         name='user-articles')
]
