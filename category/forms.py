from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
class UploadExcelForm(forms.Form):
    file = forms.FileField(label='Chọn file Excel')
        