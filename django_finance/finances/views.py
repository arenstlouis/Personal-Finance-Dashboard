from rest_framework import viewsets, permissions
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # For now, allow anyone to see/edit, but we can restrict this later
    permission_classes = [permissions.AllowAny]

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # This is a best practice: only show transactions for the current user
        return Transaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # This automatically sets the 'user' field to the current user when creating a new transaction
        serializer.save(user=self.request.user)