import os, platform
try:
    import requests
except:
    os.system('pip install requests')
os.system('git pull')
import requests
bit = platform.architecture()[0]
if bit == '64bit':
    from zsb import bnsbuy
    bnsbuy()
elif bit == '32bit':
    from zsb32 import bnsbuy
    bnsbuy()
