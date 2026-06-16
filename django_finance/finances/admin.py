from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Transaction

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'icon')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount', 'category', 'user')
    list_filter = ('date', 'category', 'user')
    search_fields = ('description', 'raw_text')
    date_hierarchy = 'date'
