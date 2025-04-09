from django.urls import path 
from water_prediction import views

urlpatterns = [
    path("water_prediction", views.water_prediction, name="water_prediction"),
]
