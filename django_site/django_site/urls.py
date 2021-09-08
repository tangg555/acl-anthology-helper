"""
@Desc:
Rrinting log to both screen and files.
@Reference:
Admin文档生成器
https://docs.djangoproject.com/zh-hans/3.2/ref/contrib/admin/admindocs/
Django's admin documentation generator not working
https://stackoverflow.com/questions/28115623/djangos-admin-documentation-generator-not-working
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    # TemplateView.as_view会将template转换为view
    path('', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
    # path('login/', LoginView.as_view(), name='users.login'),
    # path('logout/', LogoutView.as_view(), name='users.logout'),
    # path('register/', RegisterView.as_view(), name='users.register'),
    # path('captcha/', include('captcha.urls')),

    # apps　
    # include((pattern_list, app_namespace), namespace=None)
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('papers/', include(('papers.urls', 'users'), namespace='papers')),
]

