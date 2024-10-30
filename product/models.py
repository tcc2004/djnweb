# product/models.py
from django.db import models
from category.models import Category
from django.utils import timezone


class Product(models.Model):
    ten = models.CharField(max_length=255)  # Tên sản phẩm
    sku = models.CharField(max_length=100, unique=True)
    mo_ta = models.TextField(blank=True, null=True)  # Mô tả sản phẩm
    gia = models.DecimalField(max_digits=10, decimal_places=2)  # Giá sản phẩm
    so_luong_ton_kho = models.PositiveIntegerField(default=0)  # Số lượng tồn kho
    ngay_san_xuat = models.DateField()  # Ngày sản xuất
    ngay_het_han = models.DateField()  # Ngày hết hạn
    hinh_anh = models.ImageField(upload_to='san_pham/', blank=True, null=True)  # Hình ảnh sản phẩm
    created_at = models.DateTimeField(auto_now_add=True)  # Ngày tạo
    updated_at = models.DateTimeField(auto_now=True)  # Ngày cập nhật
    #nha_cung_cap = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='san_phams')  # Nhà cung cấp
    #nha_san_xuat = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, related_name='san_phams')  # Nhà sản xuất
    danh_muc = models.ManyToManyField(Category, related_name='san_phams')  # Danh mục sản phẩm

    def __str__(self):
        return self.ten

    def save(self, *args, **kwargs):
        from .models import ProductPriceHistory
        # Kiểm tra xem giá có thay đổi không trước khi lưu
        if self.pk is not None:  # Kiểm tra xem sản phẩm đã tồn tại chưa (tránh khi tạo mới)
            old_product = Product.objects.get(pk=self.pk)
            if old_product.gia != self.gia:  # Nếu giá thay đổi, tạo lịch sử giá
                ProductPriceHistory.objects.create(
                    san_pham=self,
                    gia_cu=old_product.gia,
                    gia_moi=self.gia
                )
        super().save(*args, **kwargs)  # Gọi hàm save() gốc để lưu sản phẩm

    class Meta:
        indexes = [
            models.Index(fields=['ten'], name='ten_san_pham_idx'),
            models.Index(fields=['ngay_san_xuat'], name='ngay_san_xuat_idx'),
            models.Index(fields=['ngay_het_han'], name='ngay_het_han_idx'),
        ]
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
class ProductPriceHistory(models.Model):
    san_pham = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lich_su_gia')  # Sản phẩm
    gia_cu = models.DecimalField(max_digits=10, decimal_places=2)  # Giá cũ
    gia_moi = models.DecimalField(max_digits=10, decimal_places=2)  # Giá mới
    ngay_thay_doi = models.DateTimeField(auto_now_add=True)  # Ngày thay đổi giá

    def __str__(self):
        return f"Lịch sử giá của {self.san_pham.ten}: {self.gia_cu} -> {self.gia_moi}"

    class Meta:
        verbose_name = "Lịch sử giá"
        verbose_name_plural = "Lịch sử giá"
        ordering = ['-ngay_thay_doi']