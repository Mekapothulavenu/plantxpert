from django.urls import path 
from crop_recommendation import views

urlpatterns = [
    path("crop_recommendation", views.crop_recommendation, name="crop_recommendation"),
]

