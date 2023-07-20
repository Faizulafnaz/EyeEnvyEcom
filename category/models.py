from django.db import models
from offers.models import Coupon,Offer

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique = True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    category_decs = models.TextField(max_length=300, blank=True)
    cat_image = models.ImageField(upload_to="photos/categories", blank=True)
    is_available = models.BooleanField
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name



class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    brand_desc = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.brand_name
