from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from advertising.permissions import *
from rest_framework.parsers import MultiPartParser
from .models import *
from .filters import *


class AdsViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, IsNotBannedPermission]
    filterset_class = AdFilter

    def get_queryset(self):
        return self.request.user.ads.all()


class AdminCategoriesViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, SuperModelPermission]
    filterset_class = CategoryFilter


class AdminAdsViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, SuperModelPermission]
    queryset = Ad.objects.all()
    filterset_class = AdFilter


class AdminProperties(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, SuperModelPermission]
    queryset = Property.objects.all()
