from django.db import models
import random
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.
def generate_cart_id():
    """Generate a unique eight-digit cart ID."""
    while True:
        new_id = random.randint(10000000, 99999999)
        if not Cart.objects.filter(cart_id=new_id).exists():
            return new_id

class Cart(models.Model):
    cart_id = models.IntegerField(unique=True,default=generate_cart_id)
    session_id = models.TextField(default=None)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cart_id)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart =  models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.product_name    