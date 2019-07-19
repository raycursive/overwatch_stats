import requests
from functools import wraps
import logging

logger = logging.getLogger(__name__)

GAMEDATA_URL = 'https://ow.blizzard.cn/action/career/profile/gamedata'
CAREER_URL = 'https://ow.blizzard.cn/action/career/profile'


def bnet_api(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        resp = func(*args, **kwargs)
        if resp.status_code != 200:
            logger.info('call [%s] failed, 200, args:[%s] [%s]', func.__name__, args, kwargs)
            return False
        json = resp.json()
        if json.get('status'):
            if json['status'] != 'success':
                logger.info('call [%s] failed, status non-success , args:[%s] [%s]', func.__name__, args, kwargs)
                return False
            return json['data']
        return json
    return decorated


@bnet_api
def get_gamedata():
    return requests.get(GAMEDATA_URL)


@bnet_api
def get_profile(cred):
    return requests.get(CAREER_URL, cookies={
        'bnet_user_cred': cred
    })
