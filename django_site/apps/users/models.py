from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    # 自定义的性别选择规则
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    # 昵称
    nick_name = models.CharField(max_length=50, verbose_name='nick name', default='')
    # 生日，可以为空
    birthday = models.DateField(verbose_name='birthday', null=True, blank=True)
    # 性别 只能男或女，默认男
    gender = models.CharField(
        max_length=6,
        verbose_name='gender',
        choices=GENDER_CHOICES,
        default='male',
    )
    # 地址
    address = models.CharField(max_length=100, verbose_name='address', null=True, blank=True)
    # 电话
    mobile = models.CharField(max_length=11, verbose_name='telephone', null=True, blank=True)
    # 头像 默认使用default.png
    image = models.ImageField(
        max_length=100,
        upload_to='image/%Y/%m',
        default='image/default/Entity/user_default.png'
    )

    # meta信息，即后台栏目名
    class Meta:
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'

    # 重载__str__方法，打印实例会打印username，username为继承自abstract user
    def __str__(self):
        return self.username


'''
邮箱验证码
'''


class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ('register', 'register'),
        ('forget', 'retrieve your password'),
    )
    code = models.CharField(max_length=20, verbose_name='CAPTCHA')
    email = models.EmailField(max_length=50, verbose_name='email')
    send_type = models.CharField(max_length=10, choices=SEND_CHOICES, verbose_name='Verify for')
    # 这里的now得去掉(),不去掉会根据编译时间。而不是根据实例化时间。
    send_time = models.DateTimeField(default=datetime.now, verbose_name='The time of verification')

    class Meta:
        # verbose_name_plural是verbose_name的复数形式。不设置则会自动补s。
        verbose_name = 'email verification code'
        verbose_name_plural = 'email verification codes'

    def __str__(self):
        return f'{self.code}({self.email})'
