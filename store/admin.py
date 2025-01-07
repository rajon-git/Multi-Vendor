from django.contrib import admin
from .models import Category, Product, Gallery, Specification, Size, Color,Cart, CartOrder, CartOrderItem,Review

# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model = Gallery

class SpecificationAdmin(admin.TabularInline):
    model = Specification

class ColorAdmin(admin.TabularInline):
    model = Color

class SizeAdmin(admin.TabularInline):
    model = Size

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin, SpecificationAdmin, ColorAdmin, SizeAdmin]
    list_display = ['title', 'price', 'shipping_amount', 'stock_qty', 'in_stock', 'vendor','featured']
    list_editable = ['featured']
    list_filter = ['date']
    search_fields = ['title']
    

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartOrder)
admin.site.register(CartOrderItem)
admin.site.register(Review, ReviewAdmin)