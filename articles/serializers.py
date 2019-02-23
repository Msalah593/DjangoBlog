from .models import Article
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields =('title', 'body' ,'author', 'pub_date')
        read_only_fields = ( 'author' ,)
