import json
import base64
from datetime import datetime
from django.http import HttpRequest
from shapely.geometry import Point, Polygon

from rest_framework import decorators
from rest_framework.response import Response
from django.core.files.base import ContentFile

from utils.secrets import encode, decode, jsonify

from ..models import (
    Area,
    User,
    Control,
)


@decorators.api_view(http_method_names=["POST"])
def check_location(request: HttpRequest):
    data = jsonify(decode(request.data.get("data")))
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    areas = Area.objects.filter(is_active=True)

    for area in areas:
        polygon = Polygon([
            (area.alphax, area.alphay),
            (area.betax, area.betay),
            (area.gammax, area.gammay),
            (area.deltax, area.deltay),
        ])

        coordinate = Point(latitude, longitude)

        is_in_area = polygon.contains(coordinate)

        if is_in_area:
            return Response({
                "status": "success",
                "code": "",
                "data": encode(json.dumps({ "area": area.pk })),
            })
    return Response({
        "status": "error",
        "code": "",
        "data": None,
    })


@decorators.api_view(http_method_names=["POST"])
def check_handle(request: HttpRequest):
    data = jsonify(decode(request.data.get("data")))

    username = data.get("handle")

    user = User.objects.filter(username=username)

    print(data)

    if user.exists():
        user = user.first()
        return Response({
            "status": "success",
            "code": "",
            "data": user.first_name,
        })

    return Response({
        "status": "error",
        "code": "404",
        "data": None
    })


@decorators.api_view(http_method_names=["POST"])
def check_face(request: HttpRequest):
    data = jsonify(decode(request.data.get("data")))

    area = data.get("area")
    handle = data.get("handle")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    format, imgstr = request.data.get("image").split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr))
    file_name = f"control_image.{ext}"

    user = User.objects.filter(username=handle)

    if user.exists():
        user = user.first()

        now = datetime.now()

        if not user.is_active:
            return Response({
                "status": "error",
                "code": "100",
                "data": "Xodim faolsizlantirilgan."
            })

        area = Area.objects.get(pk=area)
        control = Control.objects.filter(employee=user, created__day=now.day, created__month=now.month, created__year=now.year)

        if control:
            control = control.last()
            # input
            if now.hour < user.working_time.start.hour + 4:
                print(control)
                if control.input_status == "arrived" or control.input_status == "late":
                    return Response({
                        "status": "error",
                        "code": "110",
                        "data": "Davomatdan o'tgansiz."
                    })
                else:
                    control = Control.objects.create(
                        employee=user,
                        input_area=area,
                    )
                    control.input_image.save(file_name, data, True)
                    control.save()
                    cause = ""
                    try:
                        from deepface import DeepFace
                        verify = DeepFace.verify(
                            img1_path=user.image.path,
                            img2_path=control.input_image.path,
                            anti_spoofing=True
                        )

                        if verify.get("verified"):
                            if (now.hour > user.working_time.start.hour or (now.hour == user.working_time.start.hour and now.minute > user.working_time.start.minute)):
                                control.input_status = "late"
                                control.save()
                            else:
                                control.input_status = "arrived"
                                control.save()

                            return Response({
                                "status": "success",
                                "code": "200",
                                "data": "Davomatdan o'tdingiz."
                            })
                        else:
                            if not verify.get("img2").get("right_eye") or not verify.get("img2").get("left_eye"):
                                control.input_status = "failed"
                                control.save()
                                return Response({
                                    "status": "error",
                                    "code": "120",
                                    "data": "Yuzni aniqlab bo'lmadi.",
                                })
                            else:
                                control.delete()
                                return Response({
                                    "status": "error",
                                    "code": "130",
                                    "data": "Yuzlar mos kelmadi / Boshqa xodimni ID sidan foydalanayabsiz."
                                })
                    except Exception as e:
                        cause = str(e.__cause__)

                        if cause == "Spoof detected in given image.":
                            control.input_status = "crash"
                            control.save()
                            user.is_active = False
                            user.save()

                            return Response({
                                "status": "error",
                                "code": "140",
                                "data": "Kechirasiz, siz rasm, video orqali o'tishga uringaningiz uchun tizimdan faolsizlantirildingiz."
                            })
                        print(e.__cause__)
                        print(e.__context__)
                        print(e)
            # output
            else:
                cause = ""
                try:
                    print("try")
                    from deepface import DeepFace
                    verify = DeepFace.verify(
                        img1_path=user.image.path,
                        img2_path=control.input_image.path,
                        anti_spoofing=True
                    )

                    if verify.get("verified"):
                        control.output_status = "gone"
                        control.save()

                        return Response({
                            "status": "success",
                            "code": "200",
                            "data": "Davomatdan o'tdingiz."
                        })
                    else:
                        if not verify.get("img2").get("right_eye") or not verify.get("img2").get("left_eye"):
                            control.output_status = "failed"
                            control.save()
                            return Response({
                                "status": "error",
                                "code": "120",
                                "data": "Yuzni aniqlab bo'lmadi.",
                            })
                        else:
                            return Response({
                                "status": "error",
                                "code": "130",
                                "data": "Yuzlar mos kelmadi / Boshqa xodimni ID sidan foydalanayabsiz."
                            })
                except Exception as e:
                    cause = str(e.__cause__)

                    if cause == "Spoof detected in given image.":
                        control.output_status = "crash"
                        control.save()
                        user.is_active = False
                        user.save()

                        return Response({
                            "status": "error",
                            "code": "140",
                            "data": "Kechirasiz, siz rasm, video orqali o'tishga uringaningiz uchun tizimdan faolsizlantirildingiz."
                        })
                    print(e.__context__)
                    print(e.__cause__)
                    print(e)
        else:
            # input
            if now.hour < user.working_time.start.hour + 4:
                control = Control.objects.create(
                    employee=user,
                    input_area=area,
                )
                control.input_image.save(file_name, data, True)
                control.save()

                cause = ""
                print(control)
                print(control.input_image.path)
                try:
                    print("try")
                    from deepface import DeepFace
                    verify = DeepFace.verify(
                        img1_path=user.image.path,
                        img2_path=control.input_image.path,
                        anti_spoofing=True
                    )

                    print(verify)

                    if verify.get("verified"):
                        if (now.hour > user.working_time.start.hour or (now.hour == user.working_time.start.hour and now.minute > user.working_time.start.minute)):
                            control.input_status = "late"
                            control.save()
                        else:
                            control.input_status = "arrived"
                            control.save()

                        return Response({
                            "status": "success",
                            "code": "200",
                            "data": "Davomatdan o'tdingiz."
                        })
                    else:
                        if not verify.get("img2").get("right_eye") or not verify.get("img2").get("left_eye"):
                            control.input_status = "failed"
                            control.save()
                            return Response({
                                "status": "error",
                                "code": "120",
                                "data": "Yuzni aniqlab bo'lmadi.",
                            })
                        else:
                            control.delete()
                            return Response({
                                "status": "error",
                                "code": "130",
                                "data": "Yuzlar mos kelmadi / Boshqa xodimni ID sidan foydalanayabsiz."
                            })
                except Exception as e:
                    cause = str(e.__cause__)

                    if cause == "Spoof detected in given image.":
                        control.input_status = "crash"
                        control.save()
                        user.is_active = False
                        user.save()

                        return Response({
                            "status": "error",
                            "code": "140",
                            "data": "Kechirasiz, siz rasm, video orqali o'tishga uringaningiz uchun tizimdan faolsizlantirildingiz."
                        })
                    else:
                        print(e)
            # output
            else:
                return Response({
                    "status": "error",
                    "code": "150",
                    "data": "Davomatdan o'tishga kech qoldingiz",
                })

    return Response({
        "status": "error",
        "code": "404",
        "data": None
    })
