from django import forms
from .models import Product,Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['ten', 'sku', 'mo_ta', 'gia', 'so_luong_ton_kho', 'ngay_san_xuat', 'ngay_het_han', 'hinh_anh', 'danh_muc']
        widgets = {
            'ten': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'mo_ta': forms.Textarea(attrs={'class': 'form-control'}),
            'gia': forms.NumberInput(attrs={'class': 'form-control'}),
            'so_luong_ton_kho': forms.NumberInput(attrs={'class': 'form-control'}),
            'ngay_san_xuat': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ngay_het_han': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hinh_anh': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'danh_muc': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

class ImportProductExcelForm(forms.Form):
    file = forms.FileField(label='Chọn file Excel', widget=forms.FileInput(attrs={'class': 'form-control'}))
class ProductFilterForm(forms.Form):
    ten = forms.CharField(label='Tên sản phẩm', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên sản phẩm'}))
    sku = forms.CharField(label='SKU', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SKU'}))
    gia_min = forms.DecimalField(label='Giá từ', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Giá từ'}))
    gia_max = forms.DecimalField(label='Giá đến', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Giá đến'}))
    so_luong_min = forms.IntegerField(label='Số lượng từ', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Số lượng từ'}))
    so_luong_max = forms.IntegerField(label='Số lượng đến', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Số lượng đến'}))
    
    # Thay đổi thành ModelMultipleChoiceField để chọn nhiều danh mục
    danh_muc = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label='Danh mục', required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    
    ngay_het_han_min = forms.DateField(label='Ngày hết hạn từ', required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    ngay_het_han_max = forms.DateField(label='Ngày hết hạn đến', required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))