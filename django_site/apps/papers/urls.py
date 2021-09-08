from django.urls import path

from .import views

urlpatterns = [
    path('local-papers/', views.LocalPapersView.as_view(), name='local-papers'),
    path('download-papers/', views.DownloadPapersView.as_view(), name='download-papers'),
]