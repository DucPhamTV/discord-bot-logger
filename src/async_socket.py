import asyncio

class AsyncSocket:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.reader = None
        self.writer = None

    async def init(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.ip, self.port)

    async def send(self, data):
        self.writer.write(data)
        await self.writer.drain()

        data = await self.reader.read(1024)

        self.writer.close()
        await self.writer.wait_closed()

        return data
