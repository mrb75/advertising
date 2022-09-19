from rest_framework import serializers
from .models import *
import random
from django.contrib.auth.models import Group, Permission
from django.db.models import Q


class UserImageSerializer(serializers.ModelSerializer):
    user = User

    class Meta:
        model = UserImage
        exclude = ['user']

    def create(self, validated_data):
        image = UserImage(**validated_data)
        image.user = self.context['request'].user
        image.save()
        return image


class UserImageFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = '__all__'

    def create(self, validated_data):
        image = UserImage(**validated_data)
        image.save()
        return image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        images = UserImageSerializer(many=True)
        exclude = ['date_joined', 'last_login',
                   'birth_date', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserFormSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, default=None)
    last_name = serializers.CharField(max_length=100, default=None)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(default=None)
    mobile = serializers.CharField(default=None)
    national_code = serializers.CharField(default=None)
    Gender = serializers.ChoiceField(
        choices=['Male', 'Female', 'Nothing'], default='Nothing')

    def create(self, validated_data, group=None):
        user = User(**validated_data)
        user.set_password(''.join(random.sample(
            list('abcdefghigklmnopqrstuvwxyz'), 10)))
        user.save()
        return user

    def update(self, instance, validated_data):
        user = instance
        for idx in validated_data.keys():
            if idx in ['email', 'first_name', 'last_name', 'gender', 'mobile', 'national_code']:
                setattr(user, idx, validated_data[idx])
        user.save()
        return user


class TicketSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Ticket
        fields = '__all__'


class TicketFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def create(self, validated_data):
        ticket = Ticket(**validated_data)

        ticket.save()
        return ticket


class OwnTicketFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        exclude = ['status']

    def create(self, validated_data):
        ticket = Ticket(**validated_data)
        ticket.save()
        return ticket

    def validate(self, data):
        if 'status' in data:
            raise serializers.ValidationError(
                'you cant change status of ticket.')
        return data


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class PermissionSetSerializer(serializers.Serializer):
    permission_id = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=1000)
    )


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Notification
        fields = '__all__'
