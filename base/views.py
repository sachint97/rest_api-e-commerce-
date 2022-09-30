from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.contrib.auth.hashers import make_password
from rest_framework import status


#Customizing token claims
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username
    #     token['message'] = 'Hi dummy'
    #     # ...

    #     return token # to add additional information to the encoded access/refresh token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v
        # data['user'] = self.user.username
        # data['email'] = self.user.email
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/create/',
        '/api/products/upload/',
        '/api/products/<id>/reviews/',
        '/api/products/top/',
        '/api/products/<id>/',
        '/api/products/delete/<id>',
        '/api/products/<update>/<id>',
    ]
    return Response(routes) 

@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request,pk):
    products = Product.objects.get(_id=pk)
    serializer = ProductSerializer(products, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request):
    user = request.user # after login i.e when you pass access token along with request it will automatically consist user details
    serializers=UserSerializer(user, many=False)
    return Response(serializers.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializers=UserSerializer(users, many=True)
    return Response(serializers.data)

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name = data['name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password']),
        )
        serializer = UserSerializerWithToken(user,many=False)
        return Response(serializer.data)
    except:
        return Response('Could not create user', status=status.HTTP_400_BAD_REQUEST)