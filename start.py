from lib.settings import *
from lib.COVID19 import *


covid19_info = GetCOVID19(HOSTNAME,USERNAME,PASSWORD,COVID19API)

covid19_info.menu()