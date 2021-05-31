import os

import asyncio

import aiohttp
import discord
from discord.ext import commands

from monitor import Monitor
from async_socket import AsyncSocket
from rtsp_message import RTSPMessage
from logger import log
from config import cfg, ConfigHandler

TOKEN = os.getenv('TOKEN')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.log_channel = None
        self.event_channel = None

        import socket
        hostname = socket.gethostname()
        self.monitor = Monitor(name=hostname)

        self.cameras_list = []  # ("192.168.1.4", 554), ("192.168.1.5", 554)]
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())
        self.pinger = self.loop.create_task(self.ping_to())
        self.heroku_pinger = self.loop.create_task(self.heroku_keep_alive())

    async def on_ready(self):
        log.info('Logged in as')
        log.info(self.user.name)
        log.info(self.user.id)
        log.info('------')
        self.log_channel = self.get_channel(805280434699239425)
        self.event_channel = self.get_channel(805341165293142037)


    async def ping_to(self):
        await self.wait_until_ready()
        while not self.is_closed():
            for ip, port in self.cameras_list:
                msg = RTSPMessage(ip, port).create_option_msg()
                socket = AsyncSocket(ip, port)
                try:
                    await socket.init()
                except OSError as e:
                    log.error(f"Error: {e}")
                    await self.event_channel.send(
                        f"Camera at IP: {ip} couldn't connect"
                    )
                    # send a message to events channel that
                    # unable to connect the camera
                    continue
                result = await socket.send(msg.encode())
                if b"200 OK" in result:
                    continue
                # send a message to events channels that
                # the camera responds an error code
                await self.event_channel.send(
                    f"Camera at IP: {ip} responds Error code {result}"
                )
            await asyncio.sleep(cfg.get('interval'))

    async def http_get(self, url):
        timeout = aiohttp.ClientTimeout(total=3)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                log.info(f"in http get {url}")
                async with session.get(url) as r:
                    log.info(r.status)
                    if r.status != 200:
                        return f"URL {url} response abnormal code {r.status}"
            except ClientConnectionError as e:
                log.error(e)
                return f"Unable to reach url {url}"

    async def heroku_keep_alive(self):
        await self.wait_until_ready()
        while not self.is_closed():
            for url in cfg.get('cloud_nodes'):
                log.info(url)
                msg = await self.http_get(url)
                log.info(msg)
                if msg is not None:
                    await self.event_channel.send(msg)
            await asyncio.sleep(cfg.get('interval'))

    async def my_background_task(self):
        counter = 0
        await self.wait_until_ready()
        while not self.is_closed():
            counter += 1
            result, message = await self.monitor.run()
            if result is False:
                await self.event_channel.send(message)
            elif counter % 10 == 0:
                await self.log_channel.send(message)
            #log.info(f"run status check {cfg.get('interval')}")
            await asyncio.sleep(cfg.get('interval'))


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('[BOT] Created.')


@bot.command(name="cfg")
async def update_cfg(ctx, *args):
    handler = ConfigHandler(ctx, args)
    await handler.handle()


loop = asyncio.get_event_loop()
client = MyClient()
loop.create_task(client.start(TOKEN))
loop.create_task(bot.start(TOKEN))

try:
    loop.run_forever()
finally:
    loop.close()
