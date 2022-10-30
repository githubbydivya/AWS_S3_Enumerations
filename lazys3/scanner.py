# author:   @Daniel_Abeles
# date:     26/06/18 

import os
import asyncio
from typing import List, Any

from aiohttp import ClientSession, TCPConnector
from aiohttp.resolver import AsyncResolver

from Models.response import EnumerateResponse
from .wordlist import WordlistGenerator
from .utils import (
    print_result_colored,
    fail_silently,
    print_started,
    consume_generator
)

access_dict = {200: "public", 403: "private", 404: "NotFound", 401: "private"}


class Scanner(object):
    response_list = []

    def __init__(self, wordlist_path: str, target: str, rate_limit, user_agent: str):
        self.wordlist_path = wordlist_path
        self.target = target
        self.rate_limit = rate_limit
        self.user_agent = user_agent
        # self.response_list = []

    @fail_silently
    async def _scan_single(self, bucket: str, session: ClientSession) -> List[EnumerateResponse]:
        url = f'http://{bucket}.s3.amazonaws.com'

        async with session.get(url) as response:
            await response.read()
            status_code = response.status
            access = access_dict.get(status_code)
            if not status_code == 400 and not status_code == 404:
                print(f'[Found] {url}, "access" : {access}')
            # self.response_list.append(EnumerateResponse(url, status_code))
            file_obj = open("secureu_output.txt", "a+")  # append mode
            str_to_write = url + ',' + str(status_code)
            # print(f'{str_to_write}')
            file_obj.write(str_to_write+'\n')
            file_obj.close()

    @fail_silently
    async def _scan_all(self):
        connection_args = {
            'connector': TCPConnector(limit=self.rate_limit),
            'headers': {
                'User-Agent': self.user_agent
            }
        }

        async with ClientSession(**connection_args) as session:
            await asyncio.gather(*[
                asyncio.ensure_future(self._scan_single(bucket, session))
                for bucket in WordlistGenerator(self.wordlist_path, self.target)
            ])

    @fail_silently
    def run(self):
        print_started(self.target, self.rate_limit)
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self._scan_all())
        loop.run_until_complete(future)
        return Scanner.response_list
