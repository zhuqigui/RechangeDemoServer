from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/keep_websocket_status/', consumers.FacilityConsumer),

]