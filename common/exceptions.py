from django.http import JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class ServiceUnavailableError(APIException):
    status_code = 503
    default_detail = "The requested service is unavailable!"
    default_code = "unavailable_service"


def custom_error_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    try:
        if response is None:
            data = {"message": exc.message, "status_code": 400}
            return JsonResponse(data, status=400)

        if isinstance(response.data, list):
            response.data = response.data[0]
            response.data = {
                "message": response.data,
                "status_code": response.status_code,
            }

        # checks if the raised exception is of the type you want to handle
        if isinstance(exc, ServiceUnavailableError):
            response.data = {
                "message": response.data["detail"],
                "status_code": response.status_code,
            }
    except Exception:
        pass

    # returns response as handled normally by the framework
    return response
