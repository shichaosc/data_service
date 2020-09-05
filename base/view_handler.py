from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class JsonResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, data=None, code=None, msg=None,
                 status=status.HTTP_200_OK,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = {"code": code, "message": msg, "data": data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value


class ViewSetBase(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        return JsonResponse(data=None, msg="forbidden", code=1,
                            status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        return JsonResponse(data=None, msg="forbidden", code=1,
                            status=status.HTTP_200_OK)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data, code=0, msg="success", status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, code=0, msg="success", status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return JsonResponse(data=None, msg="forbidden", code=1,
                            status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return JsonResponse(data=None, msg="forbidden", code=1,
                            status=status.HTTP_200_OK)
