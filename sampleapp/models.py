from django.db import models

# Create your models here.
class Order(models.Model):
    razorpay_order_id = models.CharField(max_length=200)
    razorpay_payment_id = models.CharField(max_length=200)
    razorpay_signature = models.TextField()
    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)
