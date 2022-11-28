from django.urls import path

from . import views

urlpatterns = [
    path('extension/youtube/<str:video_id>/', views.youtube_extension, name='api-extension-youtube'),
    path('extension/twitter/<str:reply_text>/', views.twitter_extension, name='api-extension-twitter'),
    path('website/youtube/<str:video_id>/', views.youtube_website, name='api-website-youtube')
]