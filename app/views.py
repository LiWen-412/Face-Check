import base64
import datetime
from io import BytesIO

import numpy as np
from PIL import Image
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import face_task
from .face_task import get_face_encoding
from .forms import BootstrapAuthenticationForm
from .models import User, Check

worker_time = [(9, 30), (18, 0)]  # 上班时间  9:30~18点


def checkLogin(func):
    def check(request, *args, **kwargs):
        if request.user.is_anonymous:
            return render(request, "login.html", {"form": BootstrapAuthenticationForm()})
        else:
            return func(request, *args, **kwargs)

    return check


# Create your views here.
@csrf_exempt
def index(request):
    if request.method == "GET":

        return render(request, "index.html")
    else:
        img_content = request.POST.get("img").replace("data:image/jpeg;base64,", "").replace("data:image/png;base64,",
                                                                                             "")
        img = np.array(Image.open(BytesIO(base64.b64decode(img_content))).convert("RGB"))

        img, names = get_face_encoding(img)
        img = Image.fromarray(img)
        print(names)
        b_img = BytesIO()
        img.save(b_img, "JPEG")
        now = datetime.datetime.now()
        now = (int(now.strftime("%H")), int(now.strftime("%M")))
        if now[0] > 12:
            if now[0] < worker_time[1][0] or (now[0] == worker_time[1][0] and now[0] < worker_time[1][1]):
                status = "早退"
            else:
                status = "下班"
        else:
            if now[0] < worker_time[0][0] or (now[0] == worker_time[0][0] and now[0] < worker_time[0][1]):
                status = "出勤"
            else:
                status = "迟到"

        for name in names:
            user = User.objects.get(username=name)
            Check.objects.get_or_create(user=user,
                                        status=status,
                                        day=datetime.datetime.now().date(),
                                        )

        return JsonResponse(
            {"code": 200, "data": "\n".join(names), "img": base64.b64encode(b_img.getvalue()).decode(),
             "user_check_data": [{"username": x,
                                  "date": str(datetime.datetime.now().date()),
                                  "status": status

                                  } for x in names],
             "status": status})


@csrf_exempt
def register(request):
    if request.method == "GET":

        return render(request, "register.html")
    else:
        username = request.POST.get("username")
        img1 = request.POST.get("face1").replace("data:image/jpeg;base64,",
                                                 "").replace("data:image/png;base64,", "")

        img2 = request.POST.get("face2").replace("data:image/jpeg;base64,",
                                                 "").replace("data:image/png;base64,", "")

        img3 = request.POST.get("face3").replace("data:image/jpeg;base64,",
                                                 "").replace("data:image/png;base64,", "")

        encodings = face_task.encode_face_ing(
            [np.array(Image.open(BytesIO(base64.b64decode(img1))).convert("RGB")),
             np.array(Image.open(BytesIO(base64.b64decode(img2))).convert("RGB")),
             np.array(Image.open(BytesIO(base64.b64decode(img3))).convert("RGB"))])
        if len(encodings) != 3:
            return JsonResponse({"code": 500, "msg": "您其中有一张图片没有检测到人脸哦!", })

        encodings = np.array(encodings)
        face_task.face_encodings = np.concatenate((face_task.face_encodings, encodings), axis=0)
        face_task.usernames = np.concatenate((face_task.usernames, np.array([username, username, username])), axis=0)
        np.save("names.npy", np.array(face_task.usernames))
        np.save("face_encodings.npy", face_task.face_encodings)

        password = request.POST.get("password", "")
        clss = request.POST.get("clss", "")
        pro = request.POST.get("pro", "")
        snum = request.POST.get("snum", "")
        college = request.POST.get("college", "")

        if "" in [password, clss, pro, snum, college, username]:
            return JsonResponse({"code": 500, "msg": "请填入正确的信息!", })

        user = User.objects.create_user(username=username,
                                        password=password,
                                        clss=clss,
                                        pro=pro,
                                        snum=snum,
                                        college=college,
                                        face_id=list(face_task.usernames).index(username),

                                        )

        return JsonResponse({"code": 200, "msg": "用户注册成功!", "data": {"user": user.username}})


#


from django.db.models import Q


@csrf_exempt
def search(request):
    if request.method == "GET":
        return render(request, "search.html")
    else:
        lst = []
        username = request.POST.get("username", "")
        college = request.POST.get("college", "")
        snum = request.POST.get("snum", "")
        pro = request.POST.get("pro", "")
        clss = request.POST.get("clss", "")
        date = request.POST.get("date", " - ")
        print(date)
        date1, date2 =  "", ""
        if " - " in date:
            date1, date2 = date.split(" - ")

        if username != "":
            lst.append(Q(user__username=username))

        if college != "":
            lst.append(Q(user__college=college))
        if snum != "":
            lst.append(Q(user__snum=snum))
        if pro != "":
            lst.append(Q(user__pro=pro))
        status = request.POST.get("status", "")
        if status != "":
            lst.append(Q(status=status))
        if clss != "":
            lst.append(Q(user__clss=clss))
        if len(lst) > 0:
            checks = Check.objects.filter(lst[0])
            for x in lst[1:]:
                checks = checks.filter(x)
        else:
            checks = Check.objects.all()

        if date1 != "":
            print(date1,
                  "   >>   ", date2, " >> ", date)
            date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
            date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
            checks = checks.filter(time__gte=date1, time__lte=date2)

        data = [{"username": x.user.username,
                 "time": x.time,
                 "status": x.status,
                 "pro": x.user.pro,
                 "snum": x.user.snum,
                 "college": x.user.college,
                 "clss": x.user.clss,

                 } for x in checks]

        over_time = checks.filter(status__icontains="迟到").count()
        early_time = checks.filter(status__icontains="早退").count()
        on_time = checks.filter(status__icontains="出勤").count()
        on_time_out = checks.filter(status__icontains="下班").count()
        user_data = {
            "name": '出勤统计',
            "type": 'pie',
            "radius": [30, 100],
            "data": [

            ]
        }
        if over_time:
            user_data["data"].append({"value": over_time, "name": '迟到'})
        if early_time:
            user_data["data"].append({"value": early_time, "name": '早退'})
        if on_time:
            user_data["data"].append({"value": on_time, "name": '出勤'}, )
        if on_time_out:
            user_data["data"].append({"value": on_time_out, "name": '下班'}, )

        return JsonResponse({"code": 200, "data": {"user_data": user_data, "detail": data}})
