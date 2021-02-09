"""
Singleton configuration listener
"""
import json
from pathlib import Path

from logger import log


class Config:
    DEFAULT_CFG = {
        "cameras_list": [],
        "interval": 30,
        "cloud_nodes": [],
    }
    DEFAULT_CONFIG_FILE = "/var/log/bots/discord.cfg"
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.cfg = cls.DEFAULT_CFG

        return cls._instance

    def load_config(self, path=None):
        path = path or self.DEFAULT_CONFIG_FILE
        cfg_file = Path(path)
        if not cfg_file.exists():
            log.error(f"Cannot read config from file {path}.\nLoading default config")
            self.load_default_config()
            return

        with open(path) as f:
            self.cfg = json.load(f)

        return self.cfg

    def load_default_config(self):
        self.cfg = self.DEFAULT_CFG

    def save_config(self, path=None):
        path = path or self.DEFAULT_CONFIG_FILE
        with open(path, 'w') as f:
            json.dump(cfg.cfg, f)

    def update(self, key, value):
        self.cfg.update({key: value})

    def get(self, key):
        return self.cfg.get(key)

    def get_config(self):
        return self.cfg

cfg = Config()


class ConfigHandler:
    def __init__(self, ctx, args):
        self.ctx = ctx
        self.args = args
        self.handlers = {
            "set_interval": self.set_interval,
            "show_config": self.show_cfg,
            "save_config": self.save_persistent_config,
            "load_config": self.load_cfg,
        }

    async def handle(self):
        log.info(self.args)
        try:
            handler = self.handlers.get(self.args[0])
            if handler is None:
                await self.unknown_command()
            else:
                await handler()
        except IndexError:
            await self.unknown_command()

    async def set_interval(self):
        if len(self.args) != 2:
            await self.ctx.send("Missed value after set_interval")
            return
        interval = self.args[1]
        cfg.update("interval", int(interval))
        await self.ctx.send(f"interval has been updated to {interval} seconds")

    async def show_cfg(self):
        await self.ctx.send(f"current config: {cfg.get_config()}")

    async def save_persistent_config(self):
        cfg.save_config()
        await self.ctx.send("config is saved to storage")

    async def load_cfg(self):
        loaded = cfg.load_config()
        if loaded is None:
            await self.ctx.send("Can't load config from storage, file not found")
        else:
            await self.ctx.send(f"Load config from storage{loaded}")

    async def unknown_command(self):
        config_usage = list(self.handlers)
        await self.ctx.send(f"Sorry. Wrong command. Usage:\n{config_usage}")

if __name__ == "__main__":
    print(f"{cfg.get()}")
