import requests

from .config import *
from .logging import *

URL = "/anime?airing-statuses=ongoing"
URL = URL + "&sources-exclude=ona-chinese&sources-exclude=tv-chinese&sources-exclude=movie-chinese"

def getOngoing(page=1):
    try:
        r = requests.get(url=BASE_URL+URL+"&page="+str(page))
        return r.json()
    except Exception as e:
        createLog(e)


if __name__=="__main__":
    getOngoing()