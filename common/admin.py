from django.contrib import admin
from .models import (
    Country
)

@admin.register(Country)
class CountryModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
