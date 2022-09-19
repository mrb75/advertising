from rest_framework import serializers
from .models import *
from django.db import models
from users.serializers import UserSerializer


class PropertyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyValue
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    properties = PropertyValueSerializer(read_only=True, many=True)

    class Meta:
        model = Ad
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    values = PropertyValueSerializer(read_only=True, many=True)

    class Meta:
        model = Property
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    ads = AdSerializer(read_only=True, many=True)
    properties = PropertySerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    sender = UserSerializer()
    ad = AdSerializer()

    class Meta:
        model = Message
        fields = '__all__'


class MessageFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        message = Message(**validated_data)
        message.sender = self.context['request'].user
        message.save()
        return message

    # def validate(self, attrs):
    #     if ('ad' in attrs) and ('user' in attrs):
    #         raise serializers.ValidationError('extra user field.')
    #     if 'sender' in attrs:
    #         raise serializers.ValidationError('extra sender field.')
    #     return attrs
