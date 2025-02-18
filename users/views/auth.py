import json
from django.http import HttpRequest
from rest_framework import decorators
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from utils.secrets import encode, decode, jsonify
from ..models import User, History


@decorators.api_view(http_method_names=["POST"])
def login(request: HttpRequest):
    data = jsonify(decode(request.data.get("data")))

    username = data.get("username")
    password = data.get("password")

    print(data)

    user = User.objects.filter(username=username)

    if not user.exists():
        return Response({
            "status": "error",
            "code": "404",
            "data": "Foydalanuvchi topilmadi",
        })
    
    user = user.first()

    if not user.check_password(password):
        return Response({
            "status": "error",
            "code": "400",
            "data": "Noto'g'ri parol"
        })
    
    tokens = Token.objects.filter(user=user)
    tokens.delete()
    
    token = Token.objects.create(user=user)

    History.objects.create(
        user=user,
        model="User",
        comment="Hisobga kirish",
    )
    
    return Response({
        "status": "success",
        "code": "200",
        "data": encode(json.dumps({
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "org": user.org.name if user.org else "",
            "department": user.department.name if user.department else "",
            "position": user.position,
            "role": user.role,
            "token": token.key,
        }))
    })


@decorators.api_view(http_method_names=["POST"])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
def profile(request: HttpRequest):
    user: User = request.user
    token = Token.objects.get(user=user)
    return Response({
        "status": "success",
        "code": "200",
        "data": encode(json.dumps({
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "org": user.org.name if user.org else "",
            "department": user.department.name if user.department else "",
            "position": user.position,
            "role": user.role,
            "token": token.key,
        }))
    })