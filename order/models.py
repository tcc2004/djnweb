from django.db import models, transaction
from django.core.exceptions import ValidationError
from product.models import Product
from inventory.models import Inventory, InventoryTransaction


class Order(models.Model):
    ma_don_hang = models.CharField(max_length=100, unique=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    da_huy = models.BooleanField(default=False)

    def __str__(self):
        return f"Đơn hàng {self.ma_don_hang}"

    def save(self, *args, **kwargs):
        if not self.ma_don_hang:
            self.ma_don_hang = f"DH{self.ngay_tao.strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

    @transaction.atomic
    def tao_don_hang(self, items):
        """
        Tạo đơn hàng và tự động trừ tồn kho.
        """
        for item in items:
            if item.so_luong > item.san_pham.ton_kho.so_luong:
                raise ValidationError(f"Tồn kho cho sản phẩm {item.san_pham.ten} không đủ.")

        for item in items:
            InventoryTransaction.objects.create(
                san_pham=item.san_pham,
                loai_giao_dich='xuat',
                so_luong=item.so_luong
            )
            item.save()

        self.save()


class OrderItem(models.Model):
    don_hang = models.ForeignKey(Order, related_name='chi_tiet_don_hang', on_delete=models.CASCADE)
    san_pham = models.ForeignKey(Product, on_delete=models.CASCADE)
    so_luong = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.san_pham.ten} - Số lượng: {self.so_luong}"

    def save(self, *args, **kwargs):
        inventory = Inventory.objects.get(san_pham=self.san_pham)
        if inventory.so_luong < self.so_luong:
            raise ValidationError(f"Số lượng tồn kho cho sản phẩm {self.san_pham.ten} không đủ.")
        super().save(*args, **kwargs)
