from rest_framework import routers
from .views import ArticleViewSet, UserViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'article', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls))
]
