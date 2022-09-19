from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'ads', AdsViewSet, basename='ad')
router.register(r'categories', CategoriesViewSet, basename='category')
router.register(r'messages', MessagesViewSet, basename='message')
router.register(r'messagesOperations',
                MessagesOperationsViewSet, basename='message')
urlpatterns = [
]
urlpatterns += router.urls
