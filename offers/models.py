from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.
def validate_expiry_date(value):
    min_date = date.today()
    if value < min_date:
        raise ValidationError(
            (f"Expiry date cannot be earlier than {min_date}.")
            )

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=15)
    min_amount = models.PositiveBigIntegerField()
    off_percent = models.PositiveIntegerField()
    max_discount = models.PositiveBigIntegerField()
    expiry_date = models.DateField(validators=[validate_expiry_date])


    def __str__(self) -> str:
        return self.coupon_code
    
    def is_expired(self):
        return self.expiry_date < date.today()

class Offer(models.Model):
    name = models.CharField(max_length=50)
    off_percent = models.PositiveIntegerField()
    start_date = models.DateField(validators=[validate_expiry_date])
    end_date = models.DateField()

    def __str__(self) -> str:
        return self.name
