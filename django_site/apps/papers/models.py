from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Paper(models.Model):
    title = models.CharField(max_length=50, verbose_name='title', default='')
    year = models.IntegerField(validators=[MaxValueValidator(4)], verbose_name='year', default='')
    # 字符串，地址正则表达式   用于保存URL。若 verify_exists 参数为 True (默认)， 给定的 URL 会预先检查是否存在(即URL是否被有效装入且没有返回404响应).
    url = models.URLField(max_length=200, verbose_name='url', default='')
    authors = models.CharField(max_length=200, verbose_name='authors', default='')
    abstract = models.TextField(verbose_name='abstract', default='')
    reader_desc = models.TextField(verbose_name='notes', default='')

    # meta信息，即后台栏目名
    class Meta:
        verbose_name = 'paper'
        verbose_name_plural = 'papers'

    # 重载__str__方法，打印实例会打印username，username为继承自abstract user
    def __str__(self):
        return self.title

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50, verbose_name='name', default='')
    url = models.URLField(max_length=200, verbose_name='url', default='')
    info = models.TextField(verbose_name='info', default='')
    papers = models.ManyToManyField(Paper)

    # meta信息，即后台栏目名
    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def __str__(self):
        return self.name
