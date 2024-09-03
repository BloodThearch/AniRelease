import json

from src.getOngoing import getOngoing

def getOngoingTest():
    r = getOngoing()
    with open("tests/results/getOngoingTestResult.json", 'w') as f:
        json.dump(r,f)