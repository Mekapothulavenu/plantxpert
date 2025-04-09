from django.urls import path 
from yield_prediction import views

urlpatterns = [
  path("crop_yield_prediction", views.crop_yield_prediction, name="crop_yield_prediction"),
]

