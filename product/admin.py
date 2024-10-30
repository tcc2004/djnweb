from django.contrib import admin
from .models import Product, ProductPriceHistory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('ten', 'gia', 'so_luong_ton_kho', 'created_at', 'updated_at','ngay_het_han')
    list_filter = ( 'danh_muc','ten', 'created_at', 'updated_at')
    search_fields = ('ten',)
    filter_horizontal = ('danh_muc',)

@admin.register(ProductPriceHistory)
class ProductPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('san_pham', 'gia_cu', 'gia_moi', 'ngay_thay_doi')
    list_filter = ('san_pham', 'ngay_thay_doi')
    search_fields = ('san_pham__ten',)
