from rest_framework import generics

from .models import Category
from .serializers import CategorySerializer

# LIST + CREATE CATEGORY
class CategoryListCreateView(generics.ListCreateAPIView):

    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer

# DETAIL + UPDATE + DELETE CATEGORY
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer