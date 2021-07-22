import sys
import websockets
import ssl
import asyncio as aio
import logging
import pathlib
import json

from typing import Literal
from base64 import b64encode
from get_logger import get_logger

class EpnmWebsocketListener(object):

    def __init__(
            self,
            host: str,
            username: str,
            password: str,
            output_file: pathlib.Path = pathlib.Path(__file__).resolve().parent.joinpath("epnm_output"),
            verbosity=4
        ):
        self.logger = get_logger(name='EPNM-WS', verbosity=verbosity)
        self.host = host
        self.username = username
        self.password = password
        self.output_file = pathlib.Path(output_file)
        self.logger.info(f"Incomming messages will be writen to {str(self.output_file)}")
        self.extra_headers : dict = self.get_auth_header()
        self.ssl_context : ssl.SSLContext = self.get_ssl_context()
        self.counters = {
            'received_total': 0,
            'received_ok': 0,
            'received_error': 0
        }


    def get_auth_header(self) -> dict:
        username, password = [x.encode('latin1') for x in (self.username, self.password)]
        encoded_user_pass = b64encode(b':'.join([username, password])).strip().decode('ascii')
        headers = {
            "Authorization": f"Basic {encoded_user_pass}"
        }
        return headers

    def get_ssl_context(self) -> ssl.SSLContext:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context

    def write_output(self, of, data):
        of.write(f"{json.dumps(data)}\n")

    def update_counter_ok(self):
        self.counters['received_total'] += 1
        self.counters['received_ok'] += 1

    def update_counter_error(self):
        self.counters['received_total'] += 1
        self.counters['received_error'] += 1

    async def message_handler(self, connection: websockets.WebSocketClientProtocol):
        with self.output_file.open(mode="a") as of:
            async for message in connection:
                try:
                    data = json.loads(message)
                    self.logger.debug("Received JSON message.")
                    self.update_counter_ok()
                    self.write_output(of=of, data=data)
                except Exception as e:
                    self.update_counter_error()
                    print(repr(e))
                    self.logger.error(f"Cannot parse message: {message}")

    async def consume(self, topic: Literal['inventory', 'service-activation', 'template-execution', 'alarm', 'all']):

        websocket_resource_url = f"wss://{self.host}/restconf/streams/v1/{topic}.json"
        try:
            async with websockets.connect(uri=websocket_resource_url, ssl=self.ssl_context, extra_headers=self.extra_headers) as connection:
                if connection.open:
                    self.logger.info("Connection established.")
                else:
                    self.logger.error("Failed to establish connection.")

                await self.message_handler(connection=connection)
        except websockets.exceptions.InvalidStatusCode as e:
            if "HTTP 401" in repr(e):
                self.logger.error("Received HTTP 401 Unauthorized. Check your credentials.")
                sys.exit(1)


    def run(self, topic: Literal['inventory', 'service-activation', 'template-execution', 'alarm', 'all']):
        try:
            aio.get_event_loop().run_until_complete(self.consume(topic=topic))
            aio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            self.logger.info("Received KeyboardInterrupt, Closing Connection")
        finally:
            print(f"Stats: {self.counters}")
