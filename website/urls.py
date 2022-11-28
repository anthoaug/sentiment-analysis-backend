from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='website-index'),
    path('account', views.account, name='website-account'),
    path('login', views.login, name='website-login'),
    path('logout', views.logout, name='website-logut'),
    path('signup', views.signup, name='website-signup')
]
