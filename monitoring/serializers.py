from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ActivityLog, ErrorLog

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ActivityLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ActivityLog
        fields = ['id','timestamp','user','action','method','path','ip_address','user_agent','status_code','extra']

class ErrorLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ErrorLog
        fields = ['id','timestamp','user','message','stack_trace','method','endpoint','ip_address','user_agent','status_code']
