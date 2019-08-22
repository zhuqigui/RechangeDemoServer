from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from charge.views import FacilityView, BatteryView

router=SimpleRouter()
router.register('facility',FacilityView)

urlpatterns = [
    path('battery_type/',BatteryView.as_view()),


]

urlpatterns+=router.urls