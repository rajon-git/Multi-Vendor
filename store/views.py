from django.shortcuts import render
from .models import Category, Tax, Product, Cart, CartOrder, CartOrderItem
from .serializer import CategorySerializer, ProductSerializer, CartOrderItemSerializer, CartSerializer, CartOrderSerializer
from rest_framework import generics,status
from rest_framework.permissions import AllowAny, IsAuthenticated
from userauths.models import User
from decimal import Decimal
from rest_framework.response import Response
from django.db.models import Q

# Create your views here.
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductDetailsAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['slug']
        return Product.objects.get(slug = slug)
    
class CartAPIView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        payload = request.data

        product_id = payload['product_id']
        user_id = payload['user_id']
        user_id = payload['user_id']
        qty = payload['qty']
        price = payload['price']
        shipping_amount = payload['shipping_amount']
        country = payload['country']
        size = payload['size']
        color = payload['color']
        cart_id = payload['cart_id']

        product = Product.objects.get(id = product_id)
        if user_id != 'undefined':
            user = User.objects.get(id = user_id)
        else:
            user=None
        tax = Tax.objects.filter(country=country).first()
        if tax:
            tax_rate = tax.rate / 100
        else:
            tax_rate = 0

        cart = Cart.objects.filter(cart_id = cart_id, product = product).first()

        if cart:
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * Decimal(qty)
            cart.shipping_amount = Decimal(shipping_amount) * Decimal(qty)
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.color = color
            cart.size = size
            cart.country = country
            cart.cart_id = cart_id

            service_fee_perchnatage = 10 / 100
            cart.service_fee = Decimal(service_fee_perchnatage) * cart.sub_total
            cart.total = cart.shipping_amount + cart.sub_total + cart.tax_fee + cart.service_fee
            cart.save()

            return Response({'message': 'Cart Updated Successfully'}, status=status.HTTP_200_OK)
        else:
            cart = Cart()
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * Decimal(qty)
            cart.shipping_amount = Decimal(shipping_amount) * Decimal(qty)
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.color = color
            cart.size = size
            cart.country = country
            cart.cart_id = cart_id

            service_fee_perchnatage = 10 / 100
            cart.service_fee = Decimal(service_fee_perchnatage) * cart.sub_total
            cart.total = cart.shipping_amount + cart.sub_total + cart.tax_fee + cart.service_fee
            cart.save()

            return Response({'message': 'Cart Created Successfully'}, status=status.HTTP_201_CREATED)


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        user_id = self.kwargs.get('user_id') 
        if user_id is not None:
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(Q(user=user, cart_id=cart_id) | Q(user=user))
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)
        
        return queryset
    
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny,]
    lookup_field = "cart_id"

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        user_id = self.kwargs.get('user_id') 
        if user_id is not None:
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(Q(user=user, cart_id=cart_id) | Q(user=user))
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)
        return queryset
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        total_shipping = 0.0
        total_tax = 0.0
        total_service_fee = 0.0
        total_sub_total = 0.0
        total_total = 0.0

        for cart_item in queryset:
            total_shipping += float(self.calculate_shipping(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_service_fee += float(self.calculate_service_fee(cart_item))
            total_sub_total += float(self.calculate_sub_total(cart_item))
            total_total += float(self.calculate_total(cart_item))
        
        data = {
            'shipping': total_shipping,
            'tax': total_tax,
            'service_fee': total_service_fee,
            'sub_total': total_sub_total,
            'total': total_total,
        }
        return Response(data)
    def calculate_shipping(self, cart_item):
        return cart_item.shipping_amount
    def calculate_tax(self, cart_item):
        return cart_item.tax_fee
    def calculate_service_fee(self, cart_item):
        return cart_item.service_fee
    def calculate_sub_total(self, cart_item):
        return cart_item.sub_total
    def calculate_total(self, cart_item):
        return cart_item.total