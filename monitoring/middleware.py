import traceback
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from .utils import log_activity, log_error, sanitize_data

class ErrorLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        stack = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        log_error(request, str(exception), stack_trace=stack)
       
        return JsonResponse({'detail': 'Internal Server Error', 'error': str(exception)}, status=500)

class ActivityLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
       
        try:
            response = self.get_response(request)
            status = getattr(response, 'status_code', 200)
        except Exception as e:
            
            status = 500
            raise
        finally:
            action = self.infer_action(request, response)
            
            extra = {}
            if getattr(settings, 'LOG_REQUEST_BODY', False):
                if request.content_type and 'application/json' in request.content_type:
                    try:
                        import json
                        data = json.loads(request.body.decode('utf-8') or '{}')
                        extra['body'] = sanitize_data(data)
                    except Exception:
                        pass
            log_activity(request, action=action, status_code=status, extra=extra)
        return response

    def infer_action(self, request, response):
        path = request.path.lower()
        method = request.method.upper()
        if path.endswith('/auth/login'):
            return 'login'
        if path.endswith('/auth/logout'):
            return 'logout'
        if path.endswith('/me/profile') and method in ('PUT', 'PATCH'):
            return 'profile_update'
        if method == 'POST':
            return 'create'
        if method == 'PUT' or method == 'PATCH':
            return 'update'
        if method == 'DELETE':
            return 'delete'
        return 'read'
