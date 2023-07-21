from django.db import models
from django.urls import reverse
from category.models import Category, Brand
from offers.models import Coupon, Offer





# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100, unique = True)
    slug = models.SlugField(max_length=100, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=None)
    description = models.TextField(max_length=50, blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    images = models.ImageField(upload_to="photos/categories")
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)


    def is_outofstock(self):
        return self.stock <= 0 

    def get_url(self):
        return reverse('product_details', args = [self.slug])

    def __str__(self):
        return self.product_name
    
    def get_offer_price(self):
        return int(self.price - (self.price * self.offer.off_percent / 100))
    
    def get_offer_price_by_category(self):
        return int(self.price - (self.price * self.category.offer.off_percent / 100))



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    pr_images = models.ImageField(upload_to="photos/product")

    def __str__(self):
        return self.product.product_name + 'Image'





