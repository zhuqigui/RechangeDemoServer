from rest_framework.pagination import PageNumberPagination

class WalletRecordPagination(PageNumberPagination):
    page_size = 10


class ChargeRecordOrder(PageNumberPagination):
    page_size = 3