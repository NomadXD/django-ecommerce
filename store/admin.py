from django.contrib import admin

# Register your models here.
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'material', 'color', 'price')
    list_filter = ('category', 'material', 'color')
    search_fields = ('name', 'description')