from django.contrib import admin
from .models import *

# Register your models here.

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'brand', 'stock', 'category', 'modified_date', 'is_available']
    prepopulated_fields = {'slug' : ('product_name',)}
    inlines = [ProductImageAdmin]






admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)


