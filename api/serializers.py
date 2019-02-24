from articles.models import Article
from users.models import CustomUser
from users.forms import CustomUserCreationForm
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.contrib.auth.hashers import check_password, make_password

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields =('title', 'body' ,'author', 'pub_date')
        read_only_fields = ( 'author' ,)

class SignupSerializer(serializers.ModelSerializer):
    # confirm_password = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ('username','email','password')
        # writeonly_fields = ('password')
        
    def create(self, validated_data):
        # if serializer.validated_data['username'] not in serializer.validated_data['password']:
        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.objects.create_user(**validated_data)
    
    def validate(self,data):
        user = CustomUser(**data)
         # get the password from the data
        password = data.get('password')

        errors = dict() 
        try:
             # validate the password and catch the exception
            validators.validate_password(password=password, user=CustomUser)

         # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        
        return super(SignupSerializer, self).validate(data)
    #         validated_data.pop('confirm_password')
        # return super.create(self,validated_data)
    #         # return CustomUser.objects.create_user(validated_data.get('username'),validated_data.get('email'), validated_data.get('password'))
        
    # def get_success_headers(self, data):
    #       try:
    #         return {'username': str(data[username])
    #     except (TypeError, KeyError):
    #         return {}