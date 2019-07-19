from http.cookiejar import Cookie, CookieJar
from typing import NewType, Dict, Optional, Tuple, List
from requests.cookies import RequestsCookieJar

Key = NewType('Key', str)
Domain = NewType('Domain', str)
Path = NewType('Path', str)

CookieTuple = Tuple[Key, Domain, Path]


class BnetCookieJar(RequestsCookieJar):
    _template: List[CookieTuple] = [
        ('_ntes_nuid', '.163.com', '/'),
        ('MTK_BBID', '.163.com', '/'),
        ('opt', '.battlenet.com.cn', '/'),
        ('web.id', '.battlenet.com.cn', '/'),
        ('BA-tassadar-login.key', '.battlenet.com.cn', '/'),
        ('login.key', '.battlenet.com.cn', '/'),
        ('BA-tassadar', '.battlenet.com.cn', '/login'),
        ('bnet.extra', '.battlenet.com.cn', '/login'),
    ]

    @classmethod
    def load_bnet_cookies(cls, obj):
        new = cls()
        try:
            for key, domain, path in cls._template:
                value = obj[key]
                new.set(key, value, path=path, domain=domain)
        except KeyError:
            raise KeyError('Invalid Cookies: missing keys')
        return new

    def dump_bnet_cookies(self):
        tmp = self.get_dict()
        return {key: tmp[key] for key, *_ in self._template}
