from django.db import connection
from django.http import JsonResponse


def db_health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"message": "OK"}, status=200)
    except Exception as ex:
        return JsonResponse({"error": str(ex)}, status=500)
