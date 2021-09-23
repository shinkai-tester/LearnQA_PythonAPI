import datetime
import time

import requests
import json

createTaskResponse = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
obj = json.loads(createTaskResponse.text)
token = obj["token"]
seconds = obj["seconds"]
print(obj)

current_time = datetime.datetime.now()
readyTaskTime = datetime.datetime.now() + datetime.timedelta(0, seconds)

if datetime.datetime.now() < readyTaskTime:
    checkTaskBeforeReady = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
    objCheckTaskBefore = json.loads(checkTaskBeforeReady.text)
    print(objCheckTaskBefore)
    assert objCheckTaskBefore["status"] == "Job is NOT ready", "Status is NOT ok (check before the task is ready)"
else:
    print("Time is over, can't check the task before it is ready")

time.sleep(seconds)

checkTaskAfterReady = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
objCheckTaskAfter = json.loads(checkTaskAfterReady.text)
print(objCheckTaskAfter)
assert objCheckTaskAfter["status"] == "Job is ready", "Status is NOT ok (check after the task is ready)"
assert 'result' in objCheckTaskAfter.keys(), "Result is NOT in the response keys"
