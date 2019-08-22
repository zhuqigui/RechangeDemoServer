from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

urlpatterns = [

    path('api/user/', include('user.urls')),
    path('api/chargerecord/', include('chargerecord.urls')),
    path('api/quickcharge/', include('quickcharge.urls')),
    path('api/charge/', include('charge.urls')),

]
