from django.contrib import admin
from django.urls import path, include #the include module allows us to include other files in this file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')), #Blank for our homepage, need to point it to whereever it's going so we redirect it to our tracker app's urls file
]














































"""
URL configuration for ausmif project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
