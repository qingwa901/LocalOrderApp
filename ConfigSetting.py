# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 23:39:21 2024

@author: qingw
"""

import yaml
import os
import threading
import time


class ConfigSetting:
    def __init__(self, logger, path=''):
        self.open = True
        self.path = path + 'config.yaml'
        self._config = [dict()]
        self.logger = logger
        self.Change = False
        self.LastSaveTime = None
        self.load()
        self.AutoSave()

    def save(self):
        while self.open:
            try:
                if not self.Change:
                    continue
                if not os.path.exists(self.path):
                    with open(self.path, 'a') as yamlfile:
                        yaml.dump(self._config, yamlfile)
                        self.logger.info('Config file created and saved.')
                else:
                    with open(self.path, 'w') as yamlfile:
                        yaml.dump(self._config, yamlfile)
                        self.logger.info("config write successful")
                self.Change = False
            except Exception as e:
                self.logger.error(
                    "UnknownError happen during saving config. Retry in "
                    "20 secs", exc_info=e)
            finally:
                for _ in range(20):
                    time.sleep(1)
                    if not self.open:
                        break

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as yamlfile:
                self._config = yaml.load(yamlfile, Loader=yaml.FullLoader)
                self.logger.info("config read successful")

    def SetValue(self, field, value):
        self.logger.info(f'Set {field} to {value}')
        fields = field.split('.')
        config = self._config[0]
        for field in fields[:-1]:
            if field in config:
                config = config[field]
            else:
                config[field] = dict()
                config = config[field]
        config[fields[-1]] = value
        self.Change = True

    def GetValue(self, field):
        fields = field.split('.')
        config = self._config[0]
        for field in fields:
            if field in config:
                config = config[field]
            else:
                config[field] = dict()
                return None
        return config

    def AutoSave(self):
        threading.Thread(target=self.save).start()
