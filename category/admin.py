from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.core.cache import cache

from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    actions = ['restore_category']

   