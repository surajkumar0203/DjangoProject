from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from ots_app import views
urlpatterns = [
    path('admin/',include('admin_honeypot.urls')),
    path('secret/', admin.site.urls),
    path('', include('ots_app.urls')),
] 
