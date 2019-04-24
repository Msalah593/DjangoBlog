from articles.models import Article
from users.models import CustomUser
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions


class ArticleSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username', read_only='True')

    class Meta:
        model = Article
        fields = ('id', 'title', 'body', 'pub_date', 'author', 'author_username')
        read_only_fields = ('author', 'author_username')


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=CustomUser)

        # the exception raised here different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(SignupSerializer, self).validate(data)
