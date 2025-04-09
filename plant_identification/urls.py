from django.urls import path 
from plant_identification import views


urlpatterns = [
  path('plant_identification',views.plant_identification,name='plant_identification'),
]