from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('ma_don_hang', 'ngay_tao', 'da_huy')
    list_filter = ('da_huy', 'ngay_tao')
    search_fields = ('ma_don_hang',)
    inlines = [OrderItemInline]
    readonly_fields = ('ngay_tao',)  # Chỉ đọc cho ngày tạo
    ordering = ('-ngay_tao',)  # Sắp xếp theo ngày tạo mới nhất

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('don_hang', 'san_pham', 'so_luong')
    search_fields = ('don_hang__ma_don_hang', 'san_pham__ten')
    list_select_related = ('don_hang', 'san_pham')  # Tối ưu hóa truy vấn
    ordering = ('don_hang',)  # Sắp xếp theo đơn hàng
