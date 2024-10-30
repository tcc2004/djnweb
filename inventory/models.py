# inventory/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from product.models import Product  # Liên kết với sản phẩm
from supplier.models import Supplier


class Inventory(models.Model):
    san_pham = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='ton_kho')  # Sản phẩm liên quan, OneToOne để dễ quản lý
    so_luong = models.PositiveIntegerField(default=0)  # Số lượng tồn kho hiện tại
    ngay_cap_nhat = models.DateTimeField(auto_now=True)  # Ngày cập nhật tồn kho
    on_hold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Tồn kho của {self.san_pham.ten}: {self.so_luong}"
        return f"Tồn kho của {self.san_pham.ten}: {self.so_luong} (Đang vận chuyển: {self.on_hold})"

    class Meta:
        verbose_name = "Tồn kho"
        verbose_name_plural = "Tồn kho"


class InventoryTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('nhap', 'Nhập hàng'),
        ('xuat', 'Xuất hàng'),
        ('tra', 'Trả hàng'),
    ]

    san_pham = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='giao_dich_ton_kho')  # Sản phẩm liên quan
    loai_giao_dich = models.CharField(max_length=4, choices=TRANSACTION_TYPE_CHOICES)  # Loại giao dịch (nhập hoặc xuất)
    so_luong = models.PositiveIntegerField()  # Số lượng thay đổi
    ngay_giao_dich = models.DateTimeField(auto_now_add=True)  # Ngày giao dịch
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Nhà cung cấp")

    def __str__(self):
        return f"Giao dịch {self.loai_giao_dich} {self.so_luong} {self.san_pham.ten}"

    class Meta:
        verbose_name = "Giao dịch tồn kho"
        verbose_name_plural = "Giao dịch tồn kho"
        ordering = ['-ngay_giao_dich']

    def save(self, *args, **kwargs):
        # Kiểm tra số lượng xuất hàng không lớn hơn tồn kho
        if self.loai_giao_dich == 'xuat' and self.san_pham.ton_kho.so_luong < self.so_luong:
            raise ValueError("Không thể xuất vượt quá số lượng tồn kho")
        super().save(*args, **kwargs)
    


def update_inventory(sender, instance, created, **kwargs):
    """
    Cập nhật tồn kho sau mỗi giao dịch nhập/xuất.
    """
    if created:  # Chỉ thực hiện khi giao dịch mới được tạo
        inventory = instance.san_pham.ton_kho
        
        # Cập nhật số lượng tồn kho dựa trên loại giao dịch
        if instance.loai_giao_dich == 'nhap':
            inventory.so_luong += instance.so_luong
        elif instance.loai_giao_dich == 'xuat':
            inventory.so_luong -= instance.so_luong
        elif instance.loai_giao_dich == 'tra':  # Thêm logic xử lý trả hàng
            inventory.so_luong += instance.so_luong

        inventory.save()
