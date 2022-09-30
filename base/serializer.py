from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only = True)
    _id = serializers.SerializerMethodField(read_only = True)
    isAdmin = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = User
        fields = ['_id','username','email', 'name','isAdmin']

    def get_name(self,obj): # creating a custom field and assigning the first_name to it
        name = obj.first_name
        if obj.first_name == '': # if first_name is empty then assigning email as name
            name = obj.email
        return name

    def get__id(self,obj):
        return obj.id

    def get_isAdmin(self,obj):
        return obj.is_staff

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = fields = ['_id','username','email', 'name','isAdmin','token']
    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
