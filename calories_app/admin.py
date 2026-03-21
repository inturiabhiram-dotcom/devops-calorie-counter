"""Django Admin Here"""
from django.contrib import admin
from .models import Food,Profile,PostFood
class ProfileAdmin(admin.ModelAdmin):
    """ProfileAdmin class"""
    readonly_fields = ('date',)
admin.site.register(Food)
admin.site.register(Profile)
admin.site.register(PostFood)
