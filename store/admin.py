from django.contrib import admin
from django.db import models
from .models import product,Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('product_name','price','is_available','stock','category','modified_date')

    prepopulated_fields = {'slug' : ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('Product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter  = ('Product','variation_category','variation_value','is_active')

admin.site.register(product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)



