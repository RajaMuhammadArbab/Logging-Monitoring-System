from django.conf import settings
from django.utils.timezone import now
from .models import ActivityLog, ErrorLog
import json, traceback
from django.core.mail import mail_admins
import threading
try:
    import requests
except Exception:
    requests = None

SENSITIVE_KEYS = getattr(settings, 'SENSITIVE_KEYS', {'password'})

def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

def sanitize_data(data):
    if not isinstance(data, dict):
        return None
    sanitized = {}
    for k, v in data.items():
        if k.lower() in SENSITIVE_KEYS:
            sanitized[k] = '***'
        else:
            sanitized[k] = v
    return sanitized

def log_activity(request, action='other', status_code=200, extra=None):
    try:
        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action=action,
            method=request.method,
            path=request.path,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            status_code=status_code,
            extra=extra or {},
        )
    except Exception:
        # Avoid breaking app if logging fails
        pass

def log_error(request, message, stack_trace='', status_code=None):
    try:
        ErrorLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            message=message,
            stack_trace=stack_trace[:15000],
            method=getattr(request, 'method', ''),
            endpoint=getattr(request, 'path', ''),
            ip_address=get_client_ip(request) if request else None,
            user_agent=request.META.get('HTTP_USER_AGENT', '') if request else '',
            status_code=status_code,
        )
    except Exception:
        pass

def notify_critical_async(subject, text):
    def _send():
        try:
            mail_admins(subject, text, fail_silently=True)
        except Exception:
            pass
        webhook = getattr(settings, 'SLACK_WEBHOOK_URL', '')
        if webhook and requests:
            try:
                requests.post(webhook, json={'text': f'*{subject}*\n{text}'}, timeout=3)
            except Exception:
                pass
    threading.Thread(target=_send, daemon=True).start()
