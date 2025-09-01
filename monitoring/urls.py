from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, logout_view, MeProfileView,
    ItemViewSet, ActivityLogListView, ErrorLogListView, LogStatsView
)

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = [
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', logout_view, name='logout'),
    path('me/profile', MeProfileView.as_view(), name='me-profile'),
    path('logs/activities', ActivityLogListView.as_view(), name='activity-logs'),
    path('logs/errors', ErrorLogListView.as_view(), name='error-logs'),
    path('logs/stats', LogStatsView.as_view(), name='log-stats'),
    path('', include(router.urls)),
]
