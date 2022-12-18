from django.views.generic import TemplateView
from django.urls import path, re_path
from . import views

urlpatterns = [
    # Website
    path('', views.index, name='website-index'),
    path('register', views.index, name='website-register'),
    path('login', views.index, name='website-login'),
    path('dashboard', views.index, name='website-dashboard'),
    path('logout', views.index, name='website-logout'),

    # API
    path('account/session', views.session, name='website-session'),
    path('account/login', views.login, name='website-login'),
    path('account/logout', views.logout, name='website-logout'),
    path('account/register', views.register, name='website-register'),
    path('account/follow', views.add_follower, name='website-add-follower'),
    path('account/feed', views.get_feed, name='website-get-feed')
]
