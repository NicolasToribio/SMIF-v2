from django.urls import path #Don't need to include in this file because we're not pointing anywhere else. Don't need the admin stuff either
from . import views #we want to be able to access the views file from inside this file, so we have to import it

urlpatterns = [
    path('', views.home, name="home"), #Our path to the home page is in the views file andis called home
    path('about.html', views.about, name="about"),
]