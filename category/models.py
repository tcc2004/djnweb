import pandas as pd
from django.http import HttpResponse
from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Kiểm tra tên danh mục trùng lặp trước khi lưu
        if Category.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError(f"Danh mục với tên '{self.name}' đã tồn tại.")
        super().save(*args, **kwargs)


