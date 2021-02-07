"""
Singleton configuration listener
"""
import json
from pathlib import Path

from logger import Logger

log = Logger()


class Config:
    self.DEFAULT_CFG = {
        "cameras_list": [],
        "ping_interval": 30,
        "status_check_interval": 30,
        "cloud_nodes": [],
    }
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.cfg = {}

        return cls._instance

    def load_config(self, path):
        cfg_file = Path(path)
        if not cfg_file.exists():
            log.error(f"Cannot read config from file {path}.\nLoading default config")
            self.load_default_config()
            return

        with open(path) as f:
            self.cfg = json.load(f)

    def load_default_config(self):
        self.cfg = self.DEFAULT_CFG

    def save_config(self, path):
        with open(path) as f:
            json.dump(f)
