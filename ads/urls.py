from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'ads', AdsViewSet, basename='personalAd')
router.register(r'adminAds', AdminAdsViewSet, basename='adminAd')
router.register(r'adminCategories', AdminCategoriesViewSet,
                basename='adminCategory')
router.register(r'adminProperties', AdminProperties, basename='adminProperty')
urlpatterns = [

]
urlpatterns += router.urls
