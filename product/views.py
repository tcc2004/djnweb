from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import ProductForm
from django.http import HttpResponse
import csv
import pandas as pd
from .forms import ImportProductExcelForm
from .models import Product, Category
from django.http import JsonResponse
from .forms import ProductFilterForm
from django.db import IntegrityError
import uuid

# Hiển thị danh sách sản phẩm
def product_list(request):
    # Khởi tạo queryset ban đầu
    products = Product.objects.all()

    # Tạo form lọc
    filter_form = ProductFilterForm(request.GET)

    # Áp dụng bộ lọc từ form nếu hợp lệ
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('ten'):
            products = products.filter(ten__icontains=filter_form.cleaned_data['ten'])
        
        if filter_form.cleaned_data.get('sku'):
            products = products.filter(sku__icontains=filter_form.cleaned_data['sku'])
        
        if filter_form.cleaned_data.get('gia_min'):
            products = products.filter(gia__gte=filter_form.cleaned_data['gia_min'])
        
        if filter_form.cleaned_data.get('gia_max'):
            products = products.filter(gia__lte=filter_form.cleaned_data['gia_max'])
        
        if filter_form.cleaned_data.get('so_luong_min'):
            products = products.filter(so_luong_ton_kho__gte=filter_form.cleaned_data['so_luong_min'])
        
        if filter_form.cleaned_data.get('so_luong_max'):
            products = products.filter(so_luong_ton_kho__lte=filter_form.cleaned_data['so_luong_max'])
        
        # Lọc theo nhiều danh mục
        if filter_form.cleaned_data.get('danh_muc'):
            products = products.filter(danh_muc__in=filter_form.cleaned_data['danh_muc'])
        
        if filter_form.cleaned_data.get('ngay_het_han_min'):
            products = products.filter(ngay_het_han__gte=filter_form.cleaned_data['ngay_het_han_min'])
        
        if filter_form.cleaned_data.get('ngay_het_han_max'):
            products = products.filter(ngay_het_han__lte=filter_form.cleaned_data['ngay_het_han_max'])

    # Xử lý tìm kiếm theo từ khóa (query search)
    query = request.GET.get('q', None)
    if query:
        products = products.filter(ten__icontains=query)

    # Xử lý thêm sản phẩm mới từ POST request
    if request.method == "POST":
        new_product_name = request.POST.get('new_product_name')
        if new_product_name:
            new_product = Product(ten=new_product_name)
            new_product.save()
            messages.success(request, f'Đã tạo sản phẩm "{new_product_name}" thành công!')
            return redirect('product-list')

    # Trả về template với context đầy đủ
    context = {
        'products': products,
        'filter_form': filter_form,
    }
    
    return render(request, 'product/product_list.html', context)
# Tạo sản phẩm mới
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sản phẩm đã được tạo thành công.')
            return redirect('product-list')
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})

# Cập nhật sản phẩm
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sản phẩm đã được cập nhật thành công.')
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_form.html', {'form': form})

# Xóa sản phẩm
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f'Sản phẩm "{product.ten}" đã bị xóa.')
        return redirect('product-list')
    return render(request, 'product/product_confirm_delete.html', {'object': product})

# Xóa nhiều sản phẩm
def delete_multiple_products(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_ids')
        if product_ids:
            for product_id in product_ids:
                product = get_object_or_404(Product, id=product_id)
                product.delete()
            messages.success(request, f'Đã xóa {len(product_ids)} sản phẩm.')
        else:
            messages.error(request, 'Không có sản phẩm nào được chọn để xóa.')
    return redirect('product-list')
# Xuất file Excel sản phẩm
def export_products_excel(request):
    # Lấy dữ liệu từ model Product
    products = Product.objects.all().values('ten', 'gia', 'so_luong_ton_kho', 'ngay_san_xuat', 'ngay_het_han', 'danh_muc__name')

    # Chuyển dữ liệu sang DataFrame
    df = pd.DataFrame(list(products))

    # Tạo phản hồi dưới dạng file Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'

    # Ghi dữ liệu vào file Excel
    df.to_excel(response, index=False, engine='openpyxl')

    return response

def import_products_excel(request):
    if request.method == "POST":
        form = ImportProductExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            
            try:
                # Đọc file Excel bằng Pandas
                df = pd.read_excel(excel_file)

                # Danh sách các danh mục chưa tồn tại
                missing_categories = set()

                # Kiểm tra và thu thập các danh mục chưa tồn tại
                for index, row in df.iterrows():
                    categories = [c.strip() for c in row['danh_muc__name'].split(',')]
                    for category_name in categories:
                        if not Category.objects.filter(name=category_name).exists():
                            missing_categories.add(category_name)

                # Nếu có danh mục chưa tồn tại, yêu cầu xác nhận tạo mới
                if missing_categories:
                    request.session['missing_categories'] = list(missing_categories)  
                    request.session['excel_data'] = df.to_dict() 
                    return redirect('confirm-create-categories') 

                # Tạo sản phẩm nếu không có danh mục thiếu
                for index, row in df.iterrows():
                    ten = row['ten']
                    gia = row['gia']
                    so_luong_ton_kho = row['so_luong_ton_kho']
                    ngay_san_xuat = row['ngay_san_xuat']
                    ngay_het_han = row['ngay_het_han']
                    danh_muc = row['danh_muc__name']
                    
                    # Tìm các danh mục liên quan
                    categories = [Category.objects.get(name=c.strip()) for c in danh_muc.split(',')]
                    
                    # Kiểm tra hoặc tạo SKU tự động nếu thiếu
                    sku = row.get('sku') or str(uuid.uuid4())[:8]  # Tạo SKU ngẫu nhiên nếu không có

                    # Kiểm tra trùng lặp SKU trước khi tạo sản phẩm
                    if Product.objects.filter(sku=sku).exists():
                        messages.warning(request, f"Sản phẩm với SKU '{sku}' đã tồn tại. Bỏ qua sản phẩm này.")
                        continue  # Bỏ qua sản phẩm này

                    try:
                        # Tạo sản phẩm mới
                        product = Product.objects.create(
                            ten=ten,
                            sku=sku,  # Sử dụng SKU từ file hoặc tự động tạo
                            gia=gia,
                            so_luong_ton_kho=so_luong_ton_kho,
                            ngay_san_xuat=ngay_san_xuat,
                            ngay_het_han=ngay_het_han
                        )
                        product.danh_muc.set(categories)
                        product.save()

                    except IntegrityError:
                        messages.error(request, f"Không thể thêm sản phẩm với SKU '{sku}' do lỗi trùng lặp.")

                messages.success(request, "Dữ liệu sản phẩm đã được nhập thành công!")
                return redirect('product-list')

            except Exception as e:
                messages.error(request, f"Đã xảy ra lỗi: {e}")
        else:
            messages.error(request, "Vui lòng chọn file Excel hợp lệ.")

    else:
        form = ImportProductExcelForm()

    return render(request, 'product/import_product_excel_form.html', {'form': form})
def confirm_create_categories(request):
    if request.method == "POST":
        missing_categories = request.session.get('missing_categories', [])
        excel_data = request.session.get('excel_data', {})

        
        for category_name in missing_categories:
            Category.objects.create(name=category_name)

        
        df = pd.DataFrame.from_dict(excel_data)
        for index, row in df.iterrows():
            ten = row['ten']
            gia = row['gia']
            so_luong_ton_kho = row['so_luong_ton_kho']
            ngay_san_xuat = row['ngay_san_xuat']
            ngay_het_han = row['ngay_het_han']
            danh_muc = row['danh_muc__name']

            # Tìm các danh mục liên quan
            categories = [Category.objects.get(name=c.strip()) for c in danh_muc.split(',')]

            # Tạo sản phẩm mới
            product = Product.objects.create(
                ten=ten,
                gia=gia,
                so_luong_ton_kho=so_luong_ton_kho,
                ngay_san_xuat=ngay_san_xuat,
                ngay_het_han=ngay_het_han
            )
            product.danh_muc.set(categories)
            product.save()

        # Xóa session sau khi xử lý xong
        del request.session['missing_categories']
        del request.session['excel_data']

        messages.success(request, f"Đã tạo {len(missing_categories)} danh mục mới và nhập dữ liệu sản phẩm thành công.")
        return redirect('product-list')

    # Hiển thị các danh mục chưa tồn tại để người dùng xác nhận
    missing_categories = request.session.get('missing_categories', [])
    return render(request, 'product/confirm_create_categories.html', {'missing_categories': missing_categories})
def delete_product(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return JsonResponse({'success': True})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sản phẩm không tồn tại.'})
    return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ.'})