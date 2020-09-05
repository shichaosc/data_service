import time
import socket
import logging
from django.utils.deprecation import MiddlewareMixin
import json

logger = logging.getLogger('info')


class RequestLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            body = json.loads(request.body)
        except Exception:
            body = dict()
        body.update(dict(request.POST))
        log_data = {
            'user': request.user.pk,
            'remote_address': request.META['REMOTE_ADDR'],
            'server_hostname': socket.gethostname(),
            'request_method': request.method,
            'request_path': request.get_full_path(),
            'request_params': body
        }
        logger.info(log_data)
        request.start_time = time.time()


    def process_response(self, request, response):

        if response['content-type'] == 'application/json':
            if getattr(response, 'streaming', False):
                response_body = '<<<Streaming>>>'
            else:
                response_body = response.content
        else:
            response_body = '<<<Not JSON>>>'

        log_data = {
            'user': request.user.pk,
            'remote_address': request.META['REMOTE_ADDR'],
            'server_hostname': socket.gethostname(),
            'request_method': request.method,
            'request_path': request.get_full_path(),
            'response_status': response.status_code,
            'response_body': response_body,
            'run_time': time.time() - request.start_time,
        }

        logger.info(log_data)

        return response