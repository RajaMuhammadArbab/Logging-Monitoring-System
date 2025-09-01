from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('profile_update', 'Profile Update'),
        ('create', 'Create'),
        ('read', 'Read'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='activity_logs'
    )
    action = models.CharField(max_length=32, choices=ACTION_CHOICES, default='other')
    method = models.CharField(max_length=10, blank=True, default='')
    path = models.CharField(max_length=512, blank=True, default='')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default='')
    status_code = models.PositiveIntegerField(default=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    extra = models.JSONField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['action']),
            models.Index(fields=['user']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        user_display = self.user.username if self.user else "Anonymous"
        return f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {user_display} {self.action} {self.path}"


class ErrorLog(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='error_logs'
    )
    message = models.TextField()
    stack_trace = models.TextField(blank=True, default='')
    method = models.CharField(max_length=10, blank=True, default='')
    endpoint = models.CharField(max_length=512, blank=True, default='')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default='')
    status_code = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        short_message = (self.message[:57] + "...") if len(self.message) > 60 else self.message
        return f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {short_message}"

