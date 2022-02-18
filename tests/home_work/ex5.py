import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},' \
            '{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
obj = json.loads(json_text)
key = "messages"

if key in obj:
    json_second_text = str(obj[key][1]).replace("'", '"')
    obj = json.loads(json_second_text)
    key = "message"
    if key in obj:
        print(obj[key])
    else:
        print(f"Key {key} is not in JSON")
else:
    print(f"Key {key} is not in JSON")

