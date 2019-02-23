from articles.models import Article
from users.models import CustomUser
from users.forms import CustomUserCreationForm
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields =('title', 'body' ,'author', 'pub_date')
        read_only_fields = ( 'author' ,)

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','email','password')