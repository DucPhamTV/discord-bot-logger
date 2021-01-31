"""
Monitor system status, actually it doesn't need to be async,
Just to practice asyncio
"""

import asyncio

TEMPERATURE_FILE = "/sys/class/thermal/thermal_zone0/temp"


class Monitor():
    def __init__(self, name):
        self.name = name
        self.report = {'name': name}

    async def _cmd(self, cmd):
        proc = await asyncio.create_subprocess_exec(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        
        stdout, stderr = await proc.communicate()

        return stdout

    async def get_temperature(self):
        with open(TEMPERATURE_FILE) as f:
            try:
                temperature = int(f.read().strip()) / 1000.0
            except Exception as e:
                print(f"Error: {e}")
                self.report["temperature"] = "Unable to get teperature"
                return False

        if temperature > 60:
            self.report["temperature"] = f"Temperature={temperature} exceeded 60 Celcius"
            return False

        self.report["temperature"] = temperature

        return True

    async def get_mem_usage(self):
        mem = await self._cmd("free")
        try:
            _, total, used, free, _, _, avail = mem.splitlines()[1].split()
        except Exception as e:
            print(f"Error: {e}")
            self.report["mem"] = "Unable to get used memory"
            return False
        self.report["mem"] = int(used) / int(total)

        return True

    async def get_cpu_usage(self):
        cpu = await self._cmd("mpstat")
        try:
            cpu_used = float(cpu.split(b"all")[1].split()[0])
        except Exception as e:
            print(f"Error: {e}")
            self.report["cpu"] = "Unable to get used CPU"
            return False

        if cpu_used > 0.5:
            self.report["cpu"] = f"High CPU load {cpu_used}"
            return False

        self.report["cpu"] = cpu_used
        return True

    async def run(self):
        tasks = [self.get_cpu_usage(), self.get_mem_usage(), self.get_temperature()]
        result = await asyncio.gather(*tasks)

        if False in result:
            return (False, self.report)

        return (True, self.report)

if __name__ == "__main__":
    monitor = Monitor(name="Rasp4")

    asyncio.run(monitor.run())
    print("+++++++Report++++++++")
    print(monitor.report)
