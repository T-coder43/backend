from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from markdown import Markdown


class Avatar(models.Model):
    # `Avatar` 模型仅包含一个图片字段。接收的图片将保存在 `media/avatar/年月日/` 的路径中。
    content = models.ImageField(upload_to='avatar/%Y%m%d')


class Tag(models.Model):
    """文章标签"""
    text = models.CharField(max_length=30)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text


class Category(models.Model):
    """文章分类"""
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Article(models.Model):
    # 标题图
    avatar = models.ForeignKey(
        Avatar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='article'
    )
    # 标签
    tags = models.ManyToManyField(  # 多对多的关系 1篇文章能有多个标签,1个标签可以对应多个文章
        Tag,
        blank=True,
        related_name='articles'
    )

    # 分类
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )
    # 作者
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='articles',
    )
    # 标题
    title = models.CharField(max_length=100)
    # 正文
    body = models.TextField()
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    # 修改时间
    updated = models.DateTimeField(default=timezone.now)

    # 新增方法，将 body 转换为带 html 标签的正文
    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)
        # toc 是渲染后的目录
        return md_body, md.toc

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
