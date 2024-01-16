from random import shuffle
from time import sleep
import os

from wallet import Wallet
from excel import Excel
from browser import Browser
from retry import logger
from settings import SHUFFLE_WALLETS


def run_accs(private_keys: list):
    valid_accs = 0
    excel = Excel(total_len=len(private_keys))

    for index, pk in enumerate(private_keys):
        try:
            wallet = Wallet(privatekey=pk)
            logger.info(f'{wallet.address} | STARTED | {index+1}/{len(private_keys)} (valid: {valid_accs})')

            browser = Browser(address=wallet.address)

            auth_data = wallet.get_wallet_auth()
            auth_token = browser.create_meme_session(address=wallet.address, auth_data=auth_data)
            excel.add_account(wallet=auth_token)
        except Exception as err:
            logger.error(f'{wallet.address} | {err} ({err.__class__})\n')
            wallet.status = str(err)
            

    print('\n')
    sleep(0.2)
    logger.success(f'Successfully parsed {valid_accs}/{len(private_keys)} accounts')


if __name__ == "__main__":
    if not os.path.isdir('results'): os.mkdir('results')

    with open("privatekeys.txt") as f: private_keys = f.read().splitlines()
    logger.info(f'STARTED WITH {len(private_keys)} ACCOUNTS\n')
    if SHUFFLE_WALLETS: shuffle(private_keys)

    excel = Excel(total_len=len(private_keys))

    run_accs(private_keys=private_keys)

    logger.debug(' > Exit...')
    input('')
