from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path("signup", views.signup, name="signup"),
    path("LogIn", views.log_in, name="LogIn"),
    path("logout", views.logout_req, name="logout"),
    path("update", views.updateUser, name="update"),
    path("changepass", views.changepassword, name="changepass"),
    path("forgotPassword", views.forgotPass, name="forgotPassword"),
    path('activate/<uidb64>/<token>/',views.Activate, name='activate'),  
    path('ResetPassword/<uidb64>/<token>/', views.ResetPassword, name="ResetPassword"),
    path("ResetConfirm/<email>", views.ResetConfirm, name="ResetConfirm"),
  


]