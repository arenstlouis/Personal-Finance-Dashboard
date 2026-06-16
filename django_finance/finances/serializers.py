from rest_framework import serializers
from .models import Category, User, Transaction

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'color']

class TransactionSerializer(serializers.ModelSerializer):
    # Optional: This adds a "category_name" field to the JSON 
    # so the frontend doesn't have to look up the ID.
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'date', 'description', 'raw_text', 'category', 'category_name', 'user']

        # We mark 'user' as read_only because we will
        # assign it automatically in the ViewSet later.
        read_only_fields = ['user']