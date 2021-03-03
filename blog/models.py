from django.db import models
from base.model import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=255, verbose_name=u'文章标题')
    type = models.IntegerField(verbose_name=u'文章类型', db_index=True)
    content = models.IntegerField(verbose_name=u'文章内容')
    operator = models.CharField(max_length=255, verbose_name=u'操作人')
    extra = models.TextField(verbose_name=u'额外信息', default={})

    class Meta:
        app_label = "blog"
        db_table = "blog_article"
        verbose_name = u'文章集合'
