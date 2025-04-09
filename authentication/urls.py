from django.urls import path 
from authentication import views


urlpatterns = [
  path('signup/',views.signup,name='signup'),
  path('login/',views.user_login,name='login'),
  path("logout/", views.user_logout, name="logout"), 
  path('forgot_password/',views.forgot_password, name='forgot_password'),
]


