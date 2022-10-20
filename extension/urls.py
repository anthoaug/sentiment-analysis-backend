from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('youtube/<str:video_id>/', views.youtube, name='youtube')
]