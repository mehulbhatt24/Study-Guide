from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('accounts',views.accounts,name='accounts'),
    path('post',views.post,name='post'),
    path('upload',views.upload,name='upload'),
    path('logout',views.logout,name='logout'),
    path('like_post',views.like_post,name='like_post'),
    path('profile/<str:pk>',views.profile,name='profile'),
]