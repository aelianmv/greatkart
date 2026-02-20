from django.shortcuts import render,redirect
from django.urls import path
from . import views


urlpatterns = [
    path('login/' ,views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('',views.dashboard,name='dashboard'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
    path('reset_password_validate//<uidb64>/<token>/',views.reset_password_validate,name='reset_password_validate'),
    path('resetPassword/',views.resetPassword,name='resetPassword'),

]