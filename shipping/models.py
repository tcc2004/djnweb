from django.db import models
from order.models import Order

class Shipping(models.Model):
    TRANG_THAI_CHOICES = [
        ('dang_xu_ly', 'Đang xử lý'),
        ('dang_giao', 'Đang giao hàng'),
        ('da_giao', 'Đã giao'),
        ('huy', 'Hủy giao hàng'),
    ]
    
    don_hang = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='van_chuyen')
    nha_van_chuyen = models.CharField(max_length=255)  # Tên nhà vận chuyển
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='dang_xu_ly')
    ngay_giao = models.DateField(null=True, blank=True)  # Ngày giao hàng
    ngay_du_kien = models.DateField(null=True, blank=True)  # Ngày dự kiến giao hàng

    def __str__(self):
        return f"Vận chuyển cho đơn hàng {self.don_hang.ma_don_hang}"
