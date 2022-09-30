from django.urls import path
from .views import getRoutes,getProducts,getProduct,MyTokenObtainPairView, getUser,getUsers,registerUser
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('',getRoutes,name='routes'),
    path('products/',getProducts,name='products'),
    path('product/<pk>',getProduct,name='product'),
    path('user/',getUser,name='user'),
    path('users/',getUsers,name='users'),
    path('create/user/',registerUser, name='create-user'),

    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify')
]