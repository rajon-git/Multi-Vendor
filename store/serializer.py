from rest_framework import serializers

from .models import Product, Category, Gallery, Specification,  Size, Color, Cart, CartOrder, CartOrderItem, ProductFaq, Review,Wishlist, Notification, Coupon

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True, read_only = True)
    color = ColorSerializer(many=True, read_only = True)
    size = SizeSerializer(many=True, read_only = True)
    specification = SpecificationSerializer(many=True, read_only = True)
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'image',
            'description',
            'category',
            'price',
            'old_price',
            'shipping_amount',
            'stock_qty',
            'in_stock',
            'status',
            'featured',
            'views',
            'ratings',
            'vendor',
            'gallery',
            'color',
            'size',
            'specification',
            'product_rating',
            'rating_count',
            'pid',
            'slug',
            'date',
        ]
    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3