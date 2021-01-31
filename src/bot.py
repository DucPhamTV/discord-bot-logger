import os

import asyncio

import discord

from monitor import Monitor

TOKEN = os.getenv('TOKEN')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())
        import socket
        hostname = socket.gethostname()
        self.monitor = Monitor(name=hostname)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        counter = 0
        await self.wait_until_ready()
        log_channel = self.get_channel(805280434699239425) # channel ID goes here
        event_channel = self.get_channel(805341165293142037) # channel ID goes here
        while not self.is_closed():
            counter += 1
            result, message = await self.monitor.run()
            if result is False:
                await event_channel.send(message)
            elif counter % 10 == 0:
                await log_channel.send(message)
            await asyncio.sleep(30) # task runs every 60 seconds


client = MyClient()
client.run(TOKEN)
