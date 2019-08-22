import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','xlr.settings')
django.setup()
from rest_framework.decorators import renderer_classes, api_view
from utils.renderer import PublicRender
import types
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
@api_view(['GET','POST'])
def abc(request):
    pass
print(abc.__name__)
print(abc.__class__)
print(abc.__class__.__name__)
print(isinstance('GET',types.FunctionType))
class CBA:
    pass

print(CBA.__class__.__name__)
print(CBA.__class__)
print(CBA.__name__)
CBA.aa=1
print(getattr(CBA,'aa'))