from django.urls import path
from . import views

urlpatterns = [
    path('san-pham/', views.product_list, name='product-list'),
    path('san-pham/them/', views.product_create, name='product-create'),
    path('san-pham/<int:pk>/cap-nhat/', views.product_update, name='product-update'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete-product'),
    path('san-pham/xoa-nhieu/', views.delete_multiple_products, name='delete-multiple-products'),
    path('san-pham/nhap-excel/', views.import_products_excel, name='import-products-excel'),
    path('san-pham/xuat-excel/', views.export_products_excel, name='export-products-excel'),
    path('san-pham/xac-nhan-tao-danh-muc/', views.confirm_create_categories, name='confirm-create-categories'),

]
