from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.product.product_name) + ' by ' + str(self.user.username)