from django.db import models
from login.models import User
# Create your models here.
class salegood(models.Model):
    description = models.TextField(max_length=256)
    img_url = models.ImageField(upload_to='img') # upload_to指定图片上传的途径，如果不存在则自动创建
    name = models.CharField(max_length=200)
    item_type = (
        ('book', '书本类'),
        ('food','食品类'),
        ('res', '物品类'),
        ('necessary', '日用品类'),
        ('other', '其他'),
    )
    money = models.CharField(max_length=20)
    email = models.EmailField()
    sort = models.CharField(max_length=32,choices=item_type,default='书本类')

    class Meta:
        verbose_name = '出售货物信息'
        verbose_name_plural= '出售货物信息'

    def __str__(self):
        tpl = '物品类别：{sort},图片：{img_url},邮箱：{email},价格：{money}'
        return tpl.format(sort=self.sort,img_url=self.img_url,email=self.email,money=self.money)
