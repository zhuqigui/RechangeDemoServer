import os
import random
from functools import reduce

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xlr.settings")
django.setup()

from django.test import TestCase

# Create your tests here.

from datetime import datetime
from django.utils.timezone import utc
# print(datetime.now())
#
#
# print(datetime.utcnow())
#
# print(datetime.utcnow().replace(tzinfo=utc))


from charge.models import Battery,Facility
#
# Battery.objects.create(name='铅酸36V', price_policy=0.3)
# Battery.objects.create(name='铅酸48V', price_policy=0.3)
# Battery.objects.create(name='铅酸60V', price_policy=0.5)
# Battery.objects.create(name='铅酸72V', price_policy=0.5)
# Battery.objects.create(name='锂电36V', price_policy=0.3)
# Battery.objects.create(name='锂电48V', price_policy=0.3)
# Battery.objects.create(name='锂电60V', price_policy=0.5)
# Battery.objects.create(name='锂电72V', price_policy=0.5)
# Battery.objects.create(name='磷酸铁锂60V', price_policy=0.5)
# Battery.objects.all()[0].delete()
#

# Facility.objects.create(facility_num=123456)


# order_num = random.sample(range(0,9), 9)
# print(order_num)
# res=reduce(lambda x,y:str(x)+str(y),order_num)
# print(res,type(res))
# print(len(res))

from dwebsocket.decorators import accept_websocket