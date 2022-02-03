import sys
import time
from json.decoder import JSONDecodeError
import requests

# 1
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

try:
    parsed_first_response_text = response.json()
except JSONDecodeError:
    print("First response is not a JSON format")
    sys.exit()

token_key = "token"
seconds_key = "seconds"
status_key = "status"
result_key = "result"

# 2
if token_key not in parsed_first_response_text:
    print(f"Key {token_key} is not in JSON")
    sys.exit()

token = parsed_first_response_text[token_key]
payload = {token_key: token}
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=payload)

try:
    parsed_second_response_text = response.json()
    if status_key in parsed_second_response_text:
        if parsed_second_response_text[status_key] != "Job is NOT ready":
            print("Task status is not as expected. Expected status: 'Job is NOT ready'")
    else:
        print(f"Key {status_key} is not in JSON")
except JSONDecodeError:
    print("Second response is not a JSON format")

# 3
if seconds_key in parsed_first_response_text:
    seconds = parsed_first_response_text[seconds_key]
    time.sleep(seconds)
else:
    print(f"Key {token_key} is not in JSON")

# 4
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=payload)

try:
    parsed_third_response_text = response.json()
except JSONDecodeError:
    print("Second response is not a JSON format")
    sys.exit()

if status_key in parsed_third_response_text:
    if parsed_third_response_text[status_key] != "Job is ready":
        print("Task status is not as expected. Expected status: 'Job is ready'")
else:
    print(f"Key {status_key} is not in JSON")

if result_key not in parsed_third_response_text:
    print(f"Key {status_key} is not in JSON")
