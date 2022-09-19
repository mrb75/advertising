from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from ads.models import Ad, Category
from ads.serializers import AdSerializer, CategorySerializer, MessageSerializer, MessageFormSerializer
from rest_framework import viewsets
from ads.filters import *
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import Notification
from users.serializers import NotificationSerializer
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from advertising.permissions import IsNotBannedPermission
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class AdsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ad.objects.filter(is_verified=True)
    serializer_class = AdSerializer
    filterset_class = AdFilter

    @method_decorator(cache_page(60*30))
    def list(self, request):
        return super().list(request)


class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter


class MessagesViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_class = MessageFilter
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(Q(ad__user=self.request.user) | Q(sender=self.request.user))


class MessagesOperationsViewSet(CreateModelMixin,
                                UpdateModelMixin,
                                DestroyModelMixin,
                                viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, IsNotBannedPermission]
    serializer_class = MessageFormSerializer

    def get_queryset(self):
        return self.request.user.sent_messages
