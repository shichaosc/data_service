import json
import requests
import logging

logger = logging.getLogger('info')

def fetch_get_api(url, params=None):
    '''
    调用java接口
    :param url:
    :param data: dict
    :return:
    '''

    headers = {
        'content-type': 'application/json'
    }


    logger.info('url: {}, data: {}'.format(url, params))

    try:
        result = requests.get(url, params=params, headers=headers)

        result = result.json()

        logger.info('java api, url: {}, result: {}, user_id: {}'.format(url, result, user_id))

        return result

    except Exception as e:

        logger.info('java api error, error={}'.format(e))

    return None