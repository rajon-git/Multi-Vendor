from rest_framework import serializers

from .models import Product, Category, Gallery, Specification,  Size, Color, Cart, CartOrder, CartOrderItem, ProductFaq, Review,Wishlist, Notification, Coupon

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'