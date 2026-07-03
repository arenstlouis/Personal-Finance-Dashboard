from rest_framework import serializers
from .models import Category, User, Transaction

class RegisterSerializer(serializers.ModelSerializer):
    # write_only so the hash never comes back out in an API response.
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # Must go through create_user(), not the default ModelSerializer
        # create(), so the password gets hashed via set_password() instead
        # of written to the DB as plaintext.
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )

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