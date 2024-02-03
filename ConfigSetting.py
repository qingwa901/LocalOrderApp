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
        self.path = path + 'config.yaml'
        self._config = [dict()]
        self.logger = logger
        self.Change = False
        self.LastSaveTime = None
        self.load()
        self.AutoSave()

    def save(self):
        while True:
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
                time.sleep(20)

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as yamlfile:
                self._config = yaml.load(yamlfile, Loader=yaml.FullLoader)
                self.logger.Info("config read successful")

    def ChangeValue(self, field, value):
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
                return None
        return config

    def AutoSave(self):
        SaveThreading = threading.Thread(self.save)
        SaveThreading.start()
