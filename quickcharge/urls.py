from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from quickcharge.views import QuickChargeMoney

router=SimpleRouter()
router.register('',QuickChargeMoney)


urlpatterns = [

]

urlpatterns+=router.urls