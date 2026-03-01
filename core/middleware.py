from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
import logging
import json

logger = logging.getLogger(__name__)


class StandardizeResponseMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # Paths that should bypass middleware formatting
        self.excluded_paths = [
            '/api/schema/',
            '/api/docs/',
            '/swagger/',
            '/redoc/',
            '/admin/',
        ]

    def _should_exclude(self, path):
        for excluded_path in self.excluded_paths:
            if path.startswith(excluded_path):
                return True
        
        documentation_keywords = ['schema', 'swagger', 'redoc', 'openapi']
        path_lower = path.lower()
        for keyword in documentation_keywords:
            if keyword in path_lower:
                return True
        
        return False

    def __call__(self, request):
        if self._should_exclude(request.path):
            return self.get_response(request)

        try:
            response = self.get_response(request)
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}", exc_info=True)
            return JsonResponse(
                {
                    "success": False,
                    "status_code": 500,
                    "message": "Internal server error",
                    "errors": {"detail": str(e)}
                },
                status=500
            )

        if isinstance(response, Response):
            return self._format_response(response)
        
        if hasattr(response, 'status_code'):
            return self._format_http_response(response, request)

        return response

    def _format_response(self, response):
        data = response.data
        status_code = response.status_code

        if 200 <= status_code < 300:
            formatted_response = {
                "success": True,
                "status_code": status_code,
                "message": "Request successful",
                "data": data,
            }
        else:
            formatted_response = {
                "success": False,
                "status_code": status_code,
                "message": self._get_error_message(data),
                "errors": data,
            }

        return JsonResponse(formatted_response, status=status_code)

    def _format_http_response(self, response, request):
        status_code = response.status_code

        if 200 <= status_code < 300:
            return response

        try:
            content = response.content.decode('utf-8')
            
            if response.get('Content-Type', '').startswith('application/json'):
                data = json.loads(content)
            else:
                data = {"detail": content[:200] if content else "Error occurred"}

        except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
            data = {"detail": "Error occurred"}

        error_messages = {
            400: "Bad request",
            401: "Unauthorized",
            403: "Permission denied",
            404: "Resource not found",
            405: "Method not allowed",
            409: "Conflict",
            429: "Too many requests",
            500: "Internal server error",
            502: "Bad gateway",
            503: "Service unavailable",
        }

        message = error_messages.get(status_code, "Error occurred")

        formatted_response = {
            "success": False,
            "status_code": status_code,
            "message": message,
            "errors": data if isinstance(data, dict) else {"detail": data},
        }

        return JsonResponse(formatted_response, status=status_code)

    def _get_error_message(self, data):
        if isinstance(data, dict):
            if "detail" in data:
                return data["detail"]
            return "Validation failed"
        return "Something went wrong"