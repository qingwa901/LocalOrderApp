# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 12:13:53 2024

@author: qingw
"""

import logging
import os


def CreateLogger(aName: str, FileName: str, Path='Log'):
    if not os.path.exists(Path):
        os.mkdir(Path)
    logger = logging.getLogger(aName)
    fhandler = logging.FileHandler(filename=Path + '/' + FileName, mode='a')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(logging.INFO)
    return logger
