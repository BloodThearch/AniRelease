import json

from src.getOngoing import getOngoing
from src.logging import createLog

def getOngoingTest():
    try:
        r = getOngoing()
        with open("tests/results/getOngoingTestResult.txt", 'w') as f:
            for record in r:
                f.write(f"{record[0]} - {record[1]}\n")
    except Exception as e:
        print("Error in testing onGoing function.")
        print(e)
        createLog(e)
