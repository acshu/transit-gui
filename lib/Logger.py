# -*- coding: utf-8 -*-

import logging

FORMAT = "%(message)s"
logging.basicConfig(format=FORMAT, level=logging.WARNING)
FORMAT = "%(message)s %(levelname)s %(pathname)s %(lineno)d"

logger = logging.getLogger('mainlog')