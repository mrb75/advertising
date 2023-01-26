from django.contrib import admin
from .models import Ad, Category, Property, Category, AdImage


class PropertyInline(admin.TabularInline):
    model = Ad.properties.through


class ChildInline(admin.TabularInline):
    model = Category
    fk_name = 'parent'
    verbose_name = 'child'


class ImageInline(admin.TabularInline):
    model = AdImage
    fk_name = 'ad'


class AdAdmin(admin.ModelAdmin):
    inlines = [
        PropertyInline,
        ImageInline,
    ]
    display = ['title', 'category', 'user', 'description', 'is_verified',
               'price', 'properties', 'create_date_time', 'modify_date_time']


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ChildInline,
    ]
    display = ['name', 'parent', 'create_date_time', 'modify_date_time']


admin.site.register(Ad, AdAdmin)
admin.site.register(Category, CategoryAdmin)
