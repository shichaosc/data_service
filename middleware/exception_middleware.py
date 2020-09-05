import json
import logging
import traceback
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('error')


class ExceptionBoxMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        if not issubclass(exception.__class__, Exception):
            return None
        ret_json = {
            'code': getattr(exception, 'code', 1),
            'message': getattr(exception, 'message', 'server error'),
            'data': None
        }
        response = JsonResponse(ret_json)
        _logger = logger
        _logger.error('status_code->{status_code}, error_code->{code}, url->{url}, '
                'method->{method}, param->{param}, '
                'body->{body}，traceback->{traceback}'.format(
            status_code=getattr(exception, 'status_code', 200), code=ret_json['code'], url=request.path,
            method=request.method, param=json.dumps(getattr(request, request.method, {})),
            body=request.body, traceback=traceback.format_exc()
        ))
        response.status_code = getattr(exception, 'status_code', 200)
        return response
