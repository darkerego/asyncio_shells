import base64


class Xor:

    def __init__(self, _key: str):
        self.key = _key

    def xor(self, plaintext) -> str:
        output = ""
        for i, character in enumerate(plaintext):
            output += chr(ord(character) ^ ord(self.key[i % len(self.key)]))
        return output

    def encoder(self, _cmd: str) -> bytes:
        if self.key:
            return base64.b64encode(f'{self.xor(_cmd)}'.encode())
        return _cmd.encode()

    def decoder(self, text: bytes) -> str:
        if self.key:
            return self.xor(base64.b64decode(text).decode())
        return text.decode()