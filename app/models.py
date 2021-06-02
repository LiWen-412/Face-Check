from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    pro = models.CharField("专业", max_length=32, default=None, null=True)
    clss = models.CharField("班级", max_length=32, default=None, null=True)
    snum = models.CharField("学号", max_length=32, default=None, null=True)
    college = models.CharField("学院", max_length=32, default=None, null=True)
    face_id = models.IntegerField("人脸ID",default=0)


    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username


# Create your models here.


class Check(models.Model):
    user = models.ForeignKey(User, verbose_name="用户", related_name="Check", on_delete=models.CASCADE)
    status = models.CharField("状态", max_length=32, default="正常上班")
    day = models.DateField("签到日")
    time = models.DateTimeField("签到时间", auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = "签到记录"
