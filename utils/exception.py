from rest_framework.exceptions import APIException


class TheBaseException(APIException):

    def __int__(self, detail, code):
        super().__init__(detail=detail, code=code)
