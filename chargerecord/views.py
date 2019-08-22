from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.decorators import action

from chargerecord.serializer import OrderRecordSerializer
from chargerecord.models import OrderRecord
from user.models import UserInfo
from utils.authentication import UserTokenAuthen
from utils.exception import TheBaseException
from utils.pagination import ChargeRecordOrder


class ChargeRecordView(GenericViewSet, ListModelMixin):
    queryset = OrderRecord.objects.all()
    serializer_class = OrderRecordSerializer
    authentication_classes = [UserTokenAuthen, ]
    pagination_class = ChargeRecordOrder

    def list(self, request, *args, **kwargs):
        user = request.user
        order_list = OrderRecord.objects.filter(user=user)
        page = self.paginate_queryset(order_list)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({'code': 200, 'data': serializer.data})
        serializer = self.get_serializer(order_list, many=True)

        return Response({'code': 200, 'data': serializer.data})
