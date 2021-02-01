import asyncio

from async_socket import AsyncSocket

RTSP_FIRST_LINE = "{command} rtsp://{host}:{port}/{path} RTSP/1.0\r\n"
RTSP_HEADER = "{}: {}\r\n"


class RTSPMessage:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def _generate_first_line(self, command, path=None):
        return RTSP_FIRST_LINE.format(
           command=command,
           host=self.ip,
           port=self.port,
           path=path or "",
        )

    def create_option_msg(self):
        msg = self._generate_first_line("OPTIONS")
        msg += RTSP_HEADER.format("CSeq", 1)
        msg += RTSP_HEADER.format("User-Agent", "Isee v1.0")
        msg += '\r\n'

        return msg


if __name__ == "__main__":
    print("Test sending OPTIONS request to camera")
    ip_cam = "192.168.1.9"
    port_cam = 554
    msg = RTSPMessage(ip_cam, port_cam)
    data = msg.create_option_msg()
    async def send():
        socket = AsyncSocket(ip_cam, port_cam)
        await socket.init()
        result = await socket.send(data.encode())

        print(result)

    asyncio.run(send())
