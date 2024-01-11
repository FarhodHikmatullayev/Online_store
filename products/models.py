from django.db import models

from users.models import User


class Category(models.Model):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=221)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True, upload_to='products/')
    price = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.name
