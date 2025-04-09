from django.urls import path 
from pest_prediction import views

urlpatterns = [
  path("pest_prediction",views.pest_prediction, name="pest_prediction"),
]
 
