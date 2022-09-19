from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from advertising.permissions import SuperModelPermission, SuperUserPermission
from rest_framework.parsers import MultiPartParser
from .models import UserImage, Ticket
from django.db.models import Q
from rest_framework.mixins import UpdateModelMixin
from django.utils import timezone


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication,
                              JWTAuthentication, SuperModelPermission]
    queryset = User.objects.all()

    def create(self, request):
        user_serializer = UserFormSerializer(
            data=request.data, context={'request': request})
        if user_serializer.is_valid():
            user = user_serializer.create(request.data)
            return Response(UserSerializer(user).data, status=201)
        else:
            return Response(user_serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        update_instance = User.objects.get(pk=pk)
        self.check_object_permissions(request, update_instance)
        user_serializer = UserFormSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.update(
                update_instance, request.data)
            return Response(UserSerializer(user).data, status=200)
        else:
            return Response(user_serializer.errors, status=400)


class EditProfile(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_queryset(self):
        return self.request.user

    def patch(self, request, format=None):
        user = self.get_queryset()
        profile_serializer = UserFormSerializer(data=request.data)
        if profile_serializer.is_valid():
            for idx in request.data.keys():
                if idx in ['email', 'first_name', 'last_name', 'gender', 'mobile', 'national_code']:
                    setattr(user, idx, request.data[idx])

            user.save()
            return Response(profile_serializer.data, status=200)
        else:
            return Response(profile_serializer.errors, status=403)


class UserImageViewSet(viewsets.ModelViewSet):
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_queryset(self):
        return self.request.user.images

    def partial_update(self, request, pk=0):
        pass

    def update(self, request):
        pass

    def destroy(self, request, pk=0):
        self.check_object_permissions(request, UserImage.objects.get(pk=pk))
        return super().destroy(request, pk=0)


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return self.request.user.tickets.all()

    def list(self, request):
        return Response({'result': True, 'data': self.queryset})

    def create(self, request):
        ticket_serializer = OwnTicketFormSerializer(data=request.data)
        if ticket_serializer.is_valid():
            request_data = request.data
            request_data['user'] = request.user
            ticket = ticket_serializer.create(request_data)
            return Response({'result': True, 'created_ticket': TicketSerializer(ticket).data}, status=201)
        else:
            return Response({'result': False, 'response': ticket_serializer.errors}, status=403)

    def partial_update(self, request, pk=0):
        self.check_object_permissions(request, Ticket.objects.get(pk=pk))
        super().partial_update(request, pk)

    def destroy(self, request, pk=0):
        self.check_object_permissions(request, Ticket.objects.get(pk=pk))
        super().destroy(request, pk)


class AdminTicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,
                              JWTAuthentication, SuperModelPermission]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.all()

    def list(self, request):
        return Response({'result': True, 'data': self.queryset})

    def retrieve(self, request, pk=0):
        ticket = Ticket.objects.get(pk=pk)
        self.check_object_permissions(request, ticket)
        return Response({'result': True, 'data': TicketSerializer(ticket).data})

    def create(self, request):
        ticket_serializer = TicketFormSerializer(data=request.data)
        if ticket_serializer.is_valid():
            request_data = request.data
            request_data['user'] = request.user
            ticket = ticket_serializer.create(request_data)
            return Response({'result': True, 'created_ticket': TicketSerializer(ticket).data}, status=201)
        else:
            return Response({'result': False, 'response': ticket_serializer.errors}, status=403)

    def partial_update(self, request, pk=0):
        self.check_object_permissions(request, Ticket.objects.get(pk=pk))
        super().partial_update(request, pk)

    def destroy(self, request, pk=0):
        self.check_object_permissions(request, Ticket.objects.get(pk=pk))
        super().destroy(request, pk)


class UserPermissions(ListAPIView):
    permission_classes = [IsAuthenticated, SuperUserPermission]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = PermissionSerializer

    def get_queryset(self, pk):
        user = User.objects.get(pk=pk)
        return Permission.objects.filter(user=user)

    def get(self, request, pk):
        return Response({'data': self.serializer_class(self.get_queryset(pk), many=True).data})


class ChangeUserPermissions(UpdateAPIView):
    permission_classes = [IsAuthenticated, SuperUserPermission]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_queryset(self, pk):
        return User.objects.get(pk=pk)

    def patch(self, request, pk):
        user = self.get_queryset(pk)
        permission_serializer = PermissionSetSerializer(
            data=request.data)
        if permission_serializer.is_valid():
            user.user_permissions.set(request.data['permission_id'])
            return Response(status=204)
        else:
            return Response({'errors': permission_serializer.errors}, status=400)


class ChangeUserBanStatus(UpdateModelMixin, viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, SuperModelPermission]
    queryset = User.objects.filter(is_superuser=False)

    def partial_update(self, request, pk):
        user = self.queryset.get(id=pk)
        if user.date_banned:
            user.date_banned = None
        else:
            user.date_banned = timezone.now()
            user.negetive_score += 10
        user.save()
        return Response(status=204)
