from django.urls import path 
from fertilizers_prediction import views

urlpatterns = [
    path("fertilizer_prediction",views.fertilizer_prediction, name="fertilizer_prediction"),
]
