import requests
from .cookies import BnetCookieJar


def login(creds):
    url = 'https://account.bnet.163.com/battlenet/login?inner_client_id=ow&inner_redirect_uri=http://ow.blizzard.cn/battlenet/login?redirect_url=http://ow.blizzard.cn/career/'
    sess = requests.Session()
    jar = BnetCookieJar.load_bnet_cookies(creds)
    sess.cookies = jar
    sess.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Accept-Language': 'en-CN;q=1, zh-Hans-CN;q=0.9, ja-JP;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
    })
    sess.get(url)
    return jar.get('bnet_user_cred'), jar.dump_bnet_cookies()
