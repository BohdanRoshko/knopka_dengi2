from eth_account.messages import encode_defunct
from web3 import Web3


class Wallet:
    def __init__(self, privatekey: str):
        self.privatekey = privatekey
        self.address = Web3().eth.account.from_key(privatekey).address
        self.status = 'None'


    def get_wallet_auth(self):
        text = f'''The wallet will be used for MEME allocation. If you referred friends, family, lovers or strangers, ensure this wallet has the NFT you referred.

But also...

Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you

Wallet: {self.address[:5] + "..." + self.address[-4:]}'''

        signature = Web3().eth.account.sign_message(encode_defunct(text=text), private_key=self.privatekey).signature.hex()

        return {"text": text, "signature": signature}
