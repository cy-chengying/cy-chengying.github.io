#encoding: utf-8
from django.db import models
#留言板模块
class Message(models.Model):
    username=models.CharField(max_length=256)
    title=models.CharField(max_length=512)
    content=models.TextField(max_length=256)
    publish=models.DateTimeField()

    class Meta:

        verbose_name = "留言板"
        verbose_name_plural = "留言板"

#为了显示
    def __str__(self):
        tpl = '用户:{username},    标题：{title},    内容：{content},    时间：{publish}'
        return tpl.format(username=self.username, title=self.title, content=self.content, publish=self.publish)


