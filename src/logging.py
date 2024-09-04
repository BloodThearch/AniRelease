import datetime

from .config import *

def createLog(msg):
    try:
        with open(LOGS_PATH, "a") as f:
            f.write("ERR : "+datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")+" | "+str(msg)+"\n\n")
    except Exception as e:
        print("Error while logging!")
        print(e)