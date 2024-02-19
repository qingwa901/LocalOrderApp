# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 12:13:53 2024

@author: qingw
"""

import logging
import os
import datetime


def CreateLogger(aName: str, FileName: str = None, Path='Log'):
    if not os.path.exists(Path):
        os.mkdir(Path)
    logger = logging.getLogger(aName)
    if FileName == None:
        FileName = aName
    fhandler = logging.FileHandler(
        filename=Path + '/' + FileName + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.log', mode='a')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(logging.DEBUG)
    return logger
