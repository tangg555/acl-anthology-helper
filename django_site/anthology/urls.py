from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='anthology_index'),
]