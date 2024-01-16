import aiofiles
from pyuseragents import random as random_ua
from requests import Session, post
from time import sleep
import loader
import settings
from retry import logger, retry
from excel import Excel


class Browser:
    def __init__(self, address: str):
        self.max_retries = 5
        self.proxy = settings.PROXY
        self.link = settings.PROXY_CHANGE_LINK
        self.address = address

        proxy_auth, proxy_address = self.proxy.split('@')
        self.proxy_login, self.proxy_pass = proxy_auth.removeprefix('http://').split(':')
        self.proxy_ip, self.proxy_port = proxy_address.split(':')

        self.session = Session()
        self.session.headers['user-agent'] = random_ua()

        self.change_ip()
        self.session.proxies.update({'http': self.proxy, 'https': self.proxy})


    def change_ip(self):
        if self.link not in ['https://changeip.mobileproxy.space/?proxy_key=...&format=json', '']:
            while True:
                r = self.session.get(self.link)
                if 'mobileproxy' in self.link and r.json().get('status') == 'OK':
                    # logger.debug(f'Proxy | Changed ip: {r.json()["new_ip"]}')
                    return True
                elif 'mobileproxy' not in self.link and r.status_code == 200:
                    logger.debug(f'{self.address} | Proxy | Changed ip: {r.text}')
                    return True
                logger.error(f'{self.address} | Proxy | Change IP error: {r.text} | {r.status_code} {r.reason}')
                sleep(10)


    @retry()
    def create_meme_session(self, address: str, auth_data: dict) -> str:
        self.session.headers.update({'Origin': 'https://www.memecoin.org'})

        payload = {
            "address": address,
            "delegate": address,
            "message": auth_data["text"],
            "signature": auth_data["signature"]
        }
        r = self.session.post('https://memefarm-api.memecoin.org/user/wallet-auth', json=payload)

        if r.json().get('accessToken'):
            # logger.debug(f'Authorized in MEME')
            auth_token: str | None = r.json().get('accessToken')
            self.session.headers['Authorization'] = 'Bearer ' + auth_token
            

            logger.debug(auth_token)
            return auth_token
        elif r.json().get('status') == 401 and r.json().get('error') == 'unauthorized':
            raise Exception(f'ERROR: Wallet not linked')
        else:
            raise Exception(f'ERROR: Unsupported login response: {r.text}')

