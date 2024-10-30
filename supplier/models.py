from django.db import models

class Supplier(models.Model):
    ten = models.CharField(max_length=255, verbose_name="Tên nhà cung cấp")
    dia_chi = models.TextField(verbose_name="Địa chỉ")
    so_dien_thoai = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return self.ten

    class Meta:
        verbose_name = "Nhà cung cấp"
        verbose_name_plural = "Nhà cung cấp"
