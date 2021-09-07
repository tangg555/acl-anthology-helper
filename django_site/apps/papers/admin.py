from django.contrib import admin
from .models import Author, Paper
# Register your models here.


@admin.register(Author, Paper)
class PersonAdmin(admin.ModelAdmin):
    pass
