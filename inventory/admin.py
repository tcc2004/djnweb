# inventory/admin.py
from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inventory, InventoryTransaction  # Import InventoryTransaction
from supplier.models import Supplier

# Đăng ký model Inventory
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):  # Đổi tên lớp quản lý thành InventoryAdmin
    list_display = ('san_pham', 'so_luong', 'ngay_cap_nhat')
    search_fields = ('san_pham__ten',)
    list_filter = ('ngay_cap_nhat',)

# # Đăng ký model InventoryTransaction
# @admin.register(InventoryTransaction)
# class InventoryTransactionAdmin(admin.ModelAdmin):  # Đổi tên lớp quản lý thành InventoryTransactionAdmin
#     list_display = ('san_pham', 'loai_giao_dich', 'so_luong', 'ngay_giao_dich')
#     search_fields = ('san_pham__ten',)
#     list_filter = ('loai_giao_dich', 'ngay_giao_dich')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['ten', 'dia_chi', 'so_dien_thoai', 'email']
    search_fields = ['ten', 'email']

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['san_pham', 'supplier', 'loai_giao_dich', 'so_luong', 'ngay_giao_dich']
    list_filter = ['loai_giao_dich', 'ngay_giao_dich', 'supplier']
    search_fields = ['san_pham__ten', 'supplier__ten']

# Signal cập nhật tồn kho sau khi giao dịch
@receiver(post_save, sender=InventoryTransaction)
def update_inventory(sender, instance, **kwargs):
    """ Cập nhật tồn kho sau mỗi giao dịch nhập/xuất """
    inventory = instance.san_pham.ton_kho
    if instance.loai_giao_dich == 'nhap':
        inventory.so_luong += instance.so_luong
    elif instance.loai_giao_dich == 'xuat':
        inventory.so_luong -= instance.so_luong
    inventory.save()
