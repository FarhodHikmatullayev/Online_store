from django.db import models

from products.models import Product
from users.models import User


class Savat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savat')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.product.name
