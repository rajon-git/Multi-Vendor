from django.shortcuts import render
from .models import Category, Product
from .serializer import CategorySerializer, ProductSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]