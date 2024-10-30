from django.urls import path
from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
from . import views

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('create/', CategoryCreateView.as_view(), name='categoryy-create'),
    path('update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('delete/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
    path('export-excel/', views.export_categories_excel, name='export-categories-excel'),
    path('import-excel/', views.import_categories_excel, name='import-categories-excel'),
    path('delete-multiple-categories/', views.delete_multiple_categories, name='delete-multiple-categories'),

]
