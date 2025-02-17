from django.http import HttpRequest
from rest_framework import decorators
from rest_framework.response import Response

from ..models import User, Department
from ..serializers import UserSerializer



@decorators.api_view(http_method_names=["GET"])
def get_employees(request: HttpRequest, pk: int):
    department = Department.objects.get(pk=pk)
    employees_obj = User.objects.filter(department=department)
    employees_serializer = UserSerializer(employees_obj, many=True).data
    return Response({
        "status": "success",
        "code": "200",
        "message": "Ajoyib",
        "data": {
            "employees": employees_serializer
        }
    })
