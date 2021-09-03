from django.db import models
from django.core.validators import MaxValueValidator
from papers.models import Paper


# Create your models here.
class Conference(models.Model):
    name = models.CharField(max_length=50, verbose_name='title', default='')
    year = models.IntegerField(validators=[MaxValueValidator(4)], verbose_name='year', default='')
    url = models.URLField(max_length=200, verbose_name='url', default='')
    papers = models.ManyToManyField(Paper)

    # meta信息，即后台栏目名
    class Meta:
        verbose_name = 'conference'
        verbose_name_plural = 'conferences'

    # 重载__str__方法，打印实例会打印username，username为继承自abstract user
    def __str__(self):
        return self.name
