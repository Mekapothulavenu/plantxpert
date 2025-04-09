from django.urls import path 
from plantXpert import views


urlpatterns = [
  path('',views.index,name='index'),
  path('weather',views.weather,name='weather'),
  path('agrishops',views.agrishops,name='agrishops'),
  path('news',views.news,name='news'),
  path('assistant',views.assistant,name='assistant'),
  path("contact/", views.contact, name="contact"),
  path("about_us", views.about_us, name="about_us"),
  path("Termsofservices",views.Termsofservices, name="Termsofservices"),
  path("privacy_policy",views.privacy_policy, name="privacy_policy"),

]