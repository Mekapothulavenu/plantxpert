from django.urls import path 
from Disease_prediction import views
urlpatterns = [ 
  path('plant_disease/',views.plant_disease,name='plant_disease'),
]