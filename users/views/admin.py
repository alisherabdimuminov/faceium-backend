import json
from fpdf import FPDF
from django.http import HttpRequest
from rest_framework import decorators
from datetime import datetime, timedelta
from rest_framework.response import Response

from utils.secrets import encode

from ..models import (
    User,
    Area,
    Department,
    WorkingTime,
    Branch,
    Control,
    Test,
    Question,
    Set,
)
from ..serializers import (
    UserSerializer, 
    AreaSerializer,
    DepartmentSerializer,
    WorkingTimeSerializer,
    AddUserSerializer,
    BranchSerializer,
    ControlsSerializer,
    TestSerializer,
    QuestionSerializer,
    SetSerializer,
)


class PDF(FPDF):
    def header(self):
        # Rendering logo:
        # self.image("logo.png", 5, 5, 15)
        self.set_font("helvetica", "B", 15)
        self.cell(80)
        self.cell(30, 10, "Ekologik ekspertiza markazi.", align="L")
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Platform powered by Ali", align="C")


@decorators.api_view(http_method_names=["GET"])
def get_stats(request: HttpRequest):
    users = User.objects.filter(is_active=True)
    department = Department.objects.filter(is_active=True)
    areas = Area.objects.filter(is_active=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": {
            "stats": {
                "users": users.count(),
                "departments": department.count(),
                "areas": areas.count(),
            }
        }
    })


@decorators.api_view(http_method_names=["GET"])
def get_users(request: HttpRequest):
    users_obj = User.objects.exclude(role="admin", is_active=False)
    users_serializer = UserSerializer(users_obj, many=True).data
    return Response({
        "status": "success",
        "code": "200",
        "message": "Ajoyib",
        "data": encode(json.dumps(users_serializer)),
    })


@decorators.api_view(http_method_names=["GET"])
def get_user(request: HttpRequest, uuid: str):
    user = User.objects.get(uuid=uuid)
    user_serializer = UserSerializer(user, many=False).data
    return Response({
        "status": "success",
        "code": "200",
        "data": encode(json.dumps(user_serializer)),
    })


@decorators.api_view(http_method_names=["POST"])
def add_user(request: HttpRequest):
    user_serializer = AddUserSerializer(data=request.data)

    image = request.FILES.get("image")
    print(image)

    if user_serializer.is_valid():
        user = user_serializer.save()
        if image:
            user.image = image
            user.set_password("123")
            user.save()
        return Response({
            "status": "success",
            "code": "200",
            "message": "Ajoyib",
            "data": user.uuid
        })
    else:
        errors = user_serializer.errors
        errors = {key: value[0] for key, value in errors.items()}
        return Response({
            "status": "error",
            "code": "400",
            "message": "Xatolik",
            "data": {
                "errors": errors
            },
        })
    

@decorators.api_view(http_method_names=["POST"])
def edit_user(request: HttpRequest, uuid: str):
    user_obj = User.objects.get(uuid=uuid)

    user_serializer = AddUserSerializer(user_obj, data=request.data)

    image = request.FILES.get("image")

    print(image)

    if user_serializer.is_valid():
        user = user_serializer.save()
        if image:
            user.image = image
            user.save()
        return Response({
            "status": "success",
            "code": "200",
            "message": "Ajoyib",
            "data": None
        })
    else:
        errors = user_serializer.errors
        errors = {key: value[0] for key, value in errors.items()}
        print(errors)

        return Response({
            "status": "error",
            "code": "400",
            "message": "Xatolik",
            "data": {
                "errors": errors
            }
        })


@decorators.api_view(http_method_names=["GET"])
def get_branches(request: HttpRequest):
    branches_obj = Branch.objects.all()
    branches_serializer = BranchSerializer(branches_obj, many=True).data
    return Response({
        "status": "success",
        "code": "200",
        "message": "Ajoyib",
        "data": encode(json.dumps(branches_serializer)),
    })


@decorators.api_view(http_method_names=["POST"])
def add_branch(request: HttpRequest):
    name = request.data.get("name")
    branch = Branch.objects.create(name=name)
    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })

@decorators.api_view(http_method_names=["GET"])
def get_departments(request: HttpRequest):
    departments_obj = Department.objects.exclude(is_active=False)
    departments_serializer = DepartmentSerializer(departments_obj, many=True).data
    return Response({
        "status": "success",
        "code": "200",
        "message": "Ajoyib",
        "data": encode(json.dumps(departments_serializer)),
    })


@decorators.api_view(http_method_names=["POST"])
def add_department(request: HttpRequest):
    name = request.data.get("name")
    department = Department.objects.create(name=name)
    return Response({
        "status": "success",
        "code": "200",
        "message": "Qo'shildi",
        "data": None
    })


@decorators.api_view(http_method_names=["POST"])
def edit_department(request: HttpRequest, pk: int):
    department = Department.objects.get()
    name = request.data.get("name")
    department.name = name
    department.save()
    return Response({
        "status": "success",
        "code": "200",
        "message": "O'zgartirildi",
        "data": None
    })


@decorators.api_view(http_method_names=["GET"])
def get_working_times(request: HttpRequest):
    working_times_obj = WorkingTime.objects.exclude(is_active=False)
    working_times_serializer = WorkingTimeSerializer(working_times_obj, many=True).data
    return Response({
        "status": "success",
        "code": "200",
        "message": "Ajoyib",
        "data": encode(json.dumps(working_times_serializer)),
    })


@decorators.api_view(http_method_names=["POST"])
def add_working_time(request: HttpRequest):
    name = request.data.get("name")
    start = request.data.get("start")
    end = request.data.get("end")
    working_time = WorkingTime.objects.create(name=name, start=start, end=end)
    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })


@decorators.api_view(http_method_names=["GET"])
def get_areas(request: HttpRequest):
    areas_obj = Area.objects.exclude(is_active=False)
    areas_serializer = AreaSerializer(areas_obj, many=True).data
    return Response({
        "status": "success",
        "code": "200",
        "message": "Ajoyib",
        "data": encode(json.dumps(areas_serializer))
    })


@decorators.api_view(http_method_names=["GET"])
def get_reports(request: HttpRequest):
    now = datetime.now()
    day = request.GET.get("day", now.day)
    month = request.GET.get("month", now.month)
    year = request.GET.get("year", now.year)

    controls_serializer = ControlsSerializer(User.objects.all(), many=True, context={ "day": day, "month": month, "year": year }).data
    return Response({
        "status": "success",
        "code": "200",
        "message": "Ajoyib",
        "data": encode(json.dumps(controls_serializer))
    })


@decorators.api_view(http_method_names=["GET"])
def get_report(request: HttpRequest, bid: str, did: str):
    now = datetime.now()
    start_day = request.GET.get("start_day", (now - timedelta(days=7)).day)
    start_month = request.GET.get("start_month", (now - timedelta(days=7)).month)
    start_year = request.GET.get("start_year", (now - timedelta(days=7)).year)
    end_day = request.GET.get("end_day", now.day)
    end_month = request.GET.get("end_month", now.month)
    end_year = request.GET.get("end_year", now.year)

    start_date = datetime.strptime(f"{start_day}-{start_month}-{start_year}", "%d-%m-%Y")
    end_date = datetime.strptime(f"{end_day}-{end_month}-{end_year}", "%d-%m-%Y")

    date_range = [(start_date + timedelta(days=i)).strftime("%d-%m-%Y") 
                  for i in range((end_date - start_date).days + 1)]

    controls = {}

    print(start_date, end_date, date_range)

    for date in date_range:
        day, month, year = date.split("-")
        p_date = datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y")
        users = User.objects.filter(branch__pk=bid, department__pk=did)
        print(p_date, p_date.weekday())
        if (p_date.weekday() == 6):
            controls[date] = [{
                "first_name": user.first_name,
                "last_name": user.last_name,
                "input_status": "rest",
                "input_time": None
            } for user in users]
        else:
            controls_serializer = ControlsSerializer(users, many=True, context={ "day": day, "month": month, "year": year }).data
            controls[date] = controls_serializer
    return Response({
        "status": "success",
        "code": "200",
        "message": "Ajoyib",
        "data": encode(json.dumps(controls))
    })


@decorators.api_view(http_method_names=["GET"])
def get_tests(request: HttpRequest):
    tests_obj = Test.objects.all()
    tests_serializer = TestSerializer(tests_obj, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": encode(json.dumps(tests_serializer.data))
    })


@decorators.api_view(http_method_names=["GET"])
def get_sets(request: HttpRequest):
    sets_obj = Set.objects.all()
    sets_serializer = SetSerializer(sets_obj, many=True).data
    return Response( {
        "status": "success",
        "code": "200",
        "data": encode(json.dumps(sets_serializer)),
    })


@decorators.api_view(http_method_names=["POST"])
def add_set(request: HttpRequest):
    name = request.data.get("name")
    set = Set.objects.create(name=name)
    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })

