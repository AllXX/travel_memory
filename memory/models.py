from django.db import models
from django.utils import timezone
from blog.models import *
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Account(models.Model):
    #ユーザー（ユーザー名、パスワード、メールアドレス）
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name="ユーザー名")
    #nickname = models.CharField(max_length=50,verbose_name="ニックネ-ム",blank=True)
    image = models.ImageField(blank=True,null=True,verbose_name="写真のパス",upload_to="images")
    birthplace = models.CharField(max_length=20,verbose_name="出生地",blank=True)
    registerd_at = models.DateTimeField(default=timezone.now,verbose_name="会員登録日時")

    def __str__(self):
        return str(self.user)


class Memory(models.Model):
    date = models.DateField(verbose_name="日付")
    place = models.CharField(max_length=50,verbose_name="旅行場所")
    account = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="ユーザ")
    memory_image = models.ImageField(blank=True,null=True,verbose_name="写真",upload_to="images")
    # memory_image = StdImageField(verbose_name="写真",upload_to="images", variations={"thumbnail":(500, 500)})
    weather = models.CharField(max_length=20,verbose_name="天気")
    feeling = models.CharField(max_length=2000,null=True,verbose_name="感想")

    def images(self):
        return MemoryImage.objects.filter(memory=self.id).order_by("-dt")  #昇順
        return MemoryImage.objects.filter(memory=self.id).order_by("dt")   

    def __str__(self):
        return f'{self.place}'

    def get_absolute_url(self):
    # create, update成功時の遷移先を定義
        return reverse("memory:detail", kwargs={'pk': self.pk})


class Geo(models.Model):
    memory = models.ForeignKey(Memory,on_delete=models.CASCADE,verbose_name="旅行場所",related_name='geo')
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0,verbose_name="緯度")
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0,verbose_name="経度")
    ken = models.CharField(max_length=50,verbose_name="都道府県",blank=True)

    def __str__(self):
        return f'{self.memory.place},{self.memory.account},{self.lat},{self.lng},{self.ken},{self.id}'


class MemoryImage(models.Model):
    dt = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    memory = models.ForeignKey(Memory,verbose_name='メモリー',on_delete=models.CASCADE,related_name='memory')
    image = models.ImageField(verbose_name="画像",upload_to="images")

    def __str__(self):
        return f'{self.memory.place},{self.image}'