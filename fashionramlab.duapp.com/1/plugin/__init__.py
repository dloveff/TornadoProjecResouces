#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from db import getLogger

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    try:
        __import__(module[:-3], locals(), globals())
    except ImportError as e:
        getLogger().info('[%s] %s: %s' % (module, e.__class__.__name__, e.message))
del module