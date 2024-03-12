import configparser
import os

class Config:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        if os.path.exists(config_file):
            self.config.read(config_file)

    def get(self, section, option, default=None):
        return self.config.get(section, option, fallback=default)

    def set(self, section, option, value):
        if section not in self.config:
            self.config.add_section(section)
        self.config.set(section, option, value)
        with open(self.config_file, 'w') as f:
            self.config.write(f)