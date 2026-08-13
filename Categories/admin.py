from django.contrib import admin
from .models import Category

# Register your models here.
@admin.register(Category)
class PostCategory(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description"
    )

    search_fields = (
        "name",
        "description",
    )