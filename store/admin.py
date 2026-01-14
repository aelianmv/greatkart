from django.contrib import admin
from django.db import models
from .models import product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('product_name','price','is_available','stock','category','modified_date')

    prepopulated_fields = {'slug' : ('product_name',)}


admin.site.register(product,ProductAdmin)