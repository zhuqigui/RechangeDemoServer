from django.urls import path, re_path
from rest_framework.routers import SimpleRouter,DefaultRouter

from user.views import UserView,send_email

router = DefaultRouter()
router.register('', UserView)

urlpatterns = [
    path('send_email/',send_email)
]
urlpatterns += router.urls
