from django.contrib import admin

from .models import (Car, Review,)
from .forms import ReviewAdminForm


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'review_count']
    list_filter = ['brand', 'model']
    search_fields = ['brand', 'model']
    ordering = ['-id']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    list_display = ['car', 'title']
    list_filter = ['car__brand']
    search_fields = ['car__brand', 'title']
    ordering = ['-id']

