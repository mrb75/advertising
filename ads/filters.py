import django_filters
from .models import Ad, Category, Message


class AdFilter(django_filters.FilterSet):
    class Meta:
        model = Ad
        fields = {
            'title': ['contains'],
            'category': ['exact'],
            'price': ['exact', 'gte', 'lte'],
            'properties': ['contains'],
            'date_created': ['exact', 'gte', 'lte']
        }


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'parent': ['exact'],
            'name': ['exact', 'contains'],
        }


class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = {
            'ad': ['exact'],
            'user': ['exact'],
            'sender': ['exact'],
            'text': ['exact', 'contains'],
            'date_created': ['exact', 'gte', 'lte'],
        }
