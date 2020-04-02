import sys
sys.path.append(".")
from commons import MoveToCommons
import difflib

import unittest

import os
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot


inst = MoveToCommons()
inst.handleFile('lvwiki','File:Batman v Superman poster.jpg')