from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from chargerecord.views import ChargeRecordView

router = SimpleRouter()
router.register('', ChargeRecordView)

urlpatterns = [

]
urlpatterns += router.urls
