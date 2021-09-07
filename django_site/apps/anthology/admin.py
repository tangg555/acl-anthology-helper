from django.contrib import admin
from .models import Conference
# Register your models here.


@admin.register(Conference)
class PersonAdmin(admin.ModelAdmin):
    pass
