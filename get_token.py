import browser_cookie3 as bc
import json
import sys
import os
import glob
from requests.utils import dict_from_cookiejar
from base64 import b64encode
from typing import Dict, List, AnyStr


def tostr(obj: Dict) -> str:
    return b64encode(json.dumps(obj).encode()).decode()


def generate_path() -> List[AnyStr]:
    if sys.platform == 'darwin':
        return glob.glob(os.path.expanduser('~/Library/Application Support/Google/Chrome/Profile 1/Cookies'))
    elif sys.platform.startswith('linux'):
        return glob.glob(os.path.expanduser('~/.config/google-chrome/Profile 1/Cookies')) \
            or glob.glob(os.path.expanduser('~/.config/chromium/Profile 1/Cookies')) \
            or glob.glob(os.path.expanduser('~/.config/google-chrome-beta/Profile 1/Cookies'))
    elif sys.platform == 'win32':
        win_group_policy_path = glob.glob(os.path.join(os.path.split(os.path.split(bc.windows_group_policy_path())[0])[0], 'Profile 1', 'Cookies'))
        return win_group_policy_path \
            or glob.glob(os.path.join(os.getenv('APPDATA', ''), '..\Local\\Google\\Chrome\\User Data\\Profile 1\\Cookies')) \
            or glob.glob(os.path.join(os.getenv('LOCALAPPDATA', ''), 'Google\\Chrome\\User Data\\Profile 1\\Cookies')) \
            or glob.glob(os.path.join(os.getenv('APPDATA', ''), 'Google\\Chrome\\User Data\\Profile 1\\Cookies'))
    else:
        raise NotImplementedError


def get_cookies() -> Dict:
    path = generate_path()
    _163_cookies = dict_from_cookiejar(bc.chrome(cookie_file=path, domain_name='.163.com'))
    _bnet_cookies = dict_from_cookiejar(bc.chrome(cookie_file=path, domain_name='.battlenet.com.cn'))

    keys = {
        '_ntes_nuid',
        'MTK_BBID',
        'opt',
        'web.id',
        'BA-tassadar-login.key',
        'login.key',
        'BA-tassadar',
        'bnet.extra',
    }

    return {k: v for k, v in {**_163_cookies, **_bnet_cookies}.items() if k in keys}


if __name__ == '__main__':
    cookies = get_cookies()
    if not cookies:
        print('Cookie not found! Please Sign in to Battle.net with Chrome')
    else:
        print('Congrats! Here\'s your token: \n')
        print(tostr(cookies))
