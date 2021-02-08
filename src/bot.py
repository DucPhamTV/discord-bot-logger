import os

import asyncio

import discord
from discord.ext import commands

from monitor import Monitor
from async_socket import AsyncSocket
from rtsp_message import RTSPMessage
from logger import Logger
from config import Config

TOKEN = os.getenv('TOKEN')
log = Logger()
cfg = Config()


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.log_channel = None
        self.event_channel = None

        import socket
        hostname = socket.gethostname()
        self.monitor = Monitor(name=hostname)

        self.cameras_list = [("192.168.1.4", 554), ("192.168.1.5", 554)]
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())
        self.pinger = self.loop.create_task(self.ping_to())

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
            await asyncio.sleep(30)

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
            await asyncio.sleep(30) # task runs every 60 seconds


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('[BOT] Created.')


@bot.command(name="cfg")
async def update_cfg(ctx, *args):
    print(args)

    if args[0] == "status_check_interval":
        if len(args) != 2:
            await ctx.send("Invalid update status_check_interval")
            return
        cfg.update("status_check_interval", int(args[1]))
        await ctx.send(f"status_check_interval has been updated to {args[1]}")
    elif args[0] == "show":
        await ctx.send(f"current config: {cfg.cfg}")
    else:
        await ctx.send("Sorry. I don't understand your command")


loop = asyncio.get_event_loop()
client = MyClient()
loop.create_task(client.start(TOKEN))
loop.create_task(bot.start(TOKEN))

try:
    loop.run_forever()
finally:
    loop.close()
