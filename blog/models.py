from django.db import models
from memory.models import Account
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="ユーザー")
    title = models.CharField(max_length=100,verbose_name="タイトル")
    feeling = models.CharField(max_length=2000,verbose_name="感想",)
    memory_image = models.ImageField(blank=True,null=True,verbose_name="写真のパス",upload_to='images')
    registerd_at = models.DateTimeField(default=timezone.now,verbose_name="登録日時")

    def __str__(self):
        return f'{self.user},{self.title}'


class Comment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,verbose_name="ブログ")
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="ユーザー")
    comment = models.CharField(max_length=200,verbose_name="コメント")

    def __str__(self):
        return f'{self.user},{self.comment}'


class Like(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,verbose_name="ブログ")
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="ユーザー")
    timestamp = models.DateField(default=timezone.now,verbose_name="登録日時")

    def __str__(self):
        return f'{self.user},{self.blog}'