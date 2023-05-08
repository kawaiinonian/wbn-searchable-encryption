from typing import Dict

import sys
import os
sys.path.append(os.getcwd() + '/project/shell/')

from utils.datatype import *

username = str()

XSETS = Dict[str, Dict[bytes, bytes]]

USETS = Dict[str, Dict[bytes, bytes]]

ASETS = Dict[str, Dict[bytes, Aset_item]]

