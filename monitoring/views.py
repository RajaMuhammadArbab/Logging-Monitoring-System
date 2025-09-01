from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.db import models
from django.db.models import Count
from django.http import HttpResponse, JsonResponse

from rest_framework import serializers, generics, permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer, ProfileUpdateSerializer,
    ActivityLogSerializer, ErrorLogSerializer
)
from .models import ActivityLog, ErrorLog
from .permissions import IsAdmin
from .utils import log_activity

User = get_user_model()


class LoginView(TokenObtainPairView):

    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    token = request.data.get('refresh')
    if token:
        try:
            t = RefreshToken(token)
            t.blacklist()
        except Exception:
            pass
    return Response({'detail': 'Logged out'})



class MeProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user



class Item(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().select_related('owner')
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class ActivityLogListView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = ActivityLog.objects.select_related('user')
        user_id = self.request.query_params.get('user_id')
        action = self.request.query_params.get('action')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if user_id:
            qs = qs.filter(user_id=user_id)
        if action:
            qs = qs.filter(action=action)
        if date_from:
            qs = qs.filter(timestamp__gte=date_from)
        if date_to:
            qs = qs.filter(timestamp__lte=date_to)
        return qs

    def list(self, request, *args, **kwargs):
        export = request.query_params.get('export')
        qs = self.get_queryset()
        if export == 'csv':
            import csv
            from io import StringIO
            f = StringIO()
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'user_id', 'action', 'method', 'path', 'ip_address', 'status_code'])
            for log in qs:
                writer.writerow([
                    log.timestamp, log.user_id, log.action,
                    log.method, log.path, log.ip_address, log.status_code
                ])
            resp = HttpResponse(f.getvalue(), content_type='text/csv')
            resp['Content-Disposition'] = 'attachment; filename=activity_logs.csv'
            return resp

        if export == 'json':
            data = ActivityLogSerializer(qs, many=True).data
            return JsonResponse(data, safe=False)

        return super().list(request, *args, **kwargs)


class ErrorLogListView(generics.ListAPIView):
    serializer_class = ErrorLogSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = ErrorLog.objects.select_related('user')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            qs = qs.filter(timestamp__gte=date_from)
        if date_to:
            qs = qs.filter(timestamp__lte=date_to)
        return qs

    def list(self, request, *args, **kwargs):
        export = request.query_params.get('export')
        qs = self.get_queryset()
        if export == 'csv':
            import csv
            from io import StringIO
            f = StringIO()
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'user_id', 'message', 'endpoint', 'status_code'])
            for log in qs:
                writer.writerow([log.timestamp, log.user_id, log.message, log.endpoint, log.status_code])
            resp = HttpResponse(f.getvalue(), content_type='text/csv')
            resp['Content-Disposition'] = 'attachment; filename=error_logs.csv'
            return resp

        if export == 'json':
            data = ErrorLogSerializer(qs, many=True).data
            return JsonResponse(data, safe=False)

        return super().list(request, *args, **kwargs)


class LogStatsView(generics.GenericAPIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        by_action = ActivityLog.objects.values('action').annotate(total=Count('id')).order_by('-total')
        daily_errors = (
            ErrorLog.objects.extra(select={'date': "date(timestamp)"})
            .values('date')
            .annotate(total=Count('id'))
            .order_by('date')
        )
        return Response({
            'by_action': list(by_action),
            'daily_errors': list(daily_errors)
        })
