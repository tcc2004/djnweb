from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from django.http import HttpResponse
import pandas as pd
from .forms import UploadExcelForm, CategoryForm
from .models import Category
from django.db.models import Q

# Danh sách các danh mục
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


# View cơ bản dùng cho tạo và cập nhật danh mục
class CategoryBaseView:
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        messages.success(self.request, "Danh mục đã được lưu thành công.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Có lỗi xảy ra, vui lòng kiểm tra lại thông tin.")
        return super().form_invalid(form)


# Tạo danh mục mới
class CategoryCreateView(CategoryBaseView, CreateView):
    def form_valid(self, form):
        messages.success(self.request, "Danh mục đã được tạo thành công.")
        return super().form_valid(form)


# Cập nhật danh mục
class CategoryUpdateView(CategoryBaseView, UpdateView):
    def form_valid(self, form):
        messages.success(self.request, "Danh mục đã được cập nhật thành công.")
        return super().form_valid(form)


# Xóa danh mục
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'Danh mục "{obj.name}" đã được xóa thành công.')
        return super().delete(request, *args, **kwargs)


def export_categories_excel(request):
    # Lấy dữ liệu từ model, không bao gồm trường image
    categories = Category.objects.filter(is_deleted=False).values('name', 'description')

    # Chuyển đổi dữ liệu thành DataFrame của pandas
    df = pd.DataFrame(categories)

    #
    # Tạo response với content type là Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="categories.xlsx"'

    # Xuất DataFrame thành file Excel
    df.to_excel(response, index=False)

    return response
def import_categories_excel(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']

            try:
                # Đọc file Excel bằng pandas
                df = pd.read_excel(excel_file)

                # Kiểm tra các cột bắt buộc có tồn tại hay không
                if 'name' not in df.columns or 'description' not in df.columns:
                    messages.error(request, "File Excel không hợp lệ. Vui lòng đảm bảo có đủ các cột 'name' và 'description'.")
                    return redirect('category-list')

                # Lặp qua từng hàng để tạo mới danh mục
                for _, row in df.iterrows():
                    # Tạo danh mục mới, Django sẽ tự động tạo ID
                    Category.objects.create(
                        name=row['name'],
                        description=row['description']
                    )

                messages.success(request, "Nhập dữ liệu thành công.")
                return redirect('category-list')

            except Exception as e:
                messages.error(request, f"Có lỗi xảy ra khi nhập dữ liệu: {str(e)}")
                return redirect('category-list')
    else:
        form = UploadExcelForm()

    return render(request, 'category/import_excel_form.html', {'form': form})

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        # Lấy từ khóa tìm kiếm từ request GET
        query = self.request.GET.get('q')
        queryset = Category.objects.filter(is_deleted=False)

        if query:
            # Tìm kiếm danh mục theo tên chứa từ khóa
            queryset = queryset.filter(Q(name__icontains=query))
            if not queryset.exists():
                # Nếu không có kết quả, hiển thị thông báo và đề xuất tạo mới
                messages.warning(self.request, f'Không tìm thấy danh mục với từ khóa "{query}". Bạn có muốn tạo mới không?')
        return queryset

    def post(self, request, *args, **kwargs):
        # Xử lý việc tạo danh mục mới từ yêu cầu tìm kiếm
        new_category_name = request.POST.get('new_category_name')
        if new_category_name:
            Category.objects.create(name=new_category_name)
            messages.success(request, f'Đã tạo danh mục "{new_category_name}" thành công.')
        return redirect('category-list')
def delete_multiple_categories(request):
    if request.method == 'POST':
        # Lấy danh sách ID danh mục từ form
        category_ids = request.POST.getlist('category_ids')

        if category_ids:
            # Xóa các danh mục có trong danh sách ID
            Category.objects.filter(id__in=category_ids).delete()
            messages.success(request, f'Đã xóa {len(category_ids)} danh mục thành công.')
        else:
            messages.error(request, 'Không có danh mục nào được chọn để xóa.')

    return redirect('category-list')