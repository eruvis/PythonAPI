import requests

# 1
print("# 1")

response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

# 2
print("\n\n# 2")

response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

# 3
print("\n\n# 3")

response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params='{"method":"GET"}')
print(f'Method GET: {response.text}')

response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data='{"method":"POST"}')
print(f'Method POST: {response.text}')

response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data='{"method":"PUT"}')
print(f'Method PUT: {response.text}')

response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data='{"method":"DELETE"}')
print(f'Method DELETE: {response.text}')

# 4
print("\n\n# 4")

methods = ["POST", "GET", "PUT", "DELETE"]

print("GET requests:")
for method in methods:
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params='{"method":"'+method+'"}')
    print(f'{method}: {response.text}')

print("\nPOST requests:")
for method in methods:
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data='{"method":"'+method+'"}')
    print(f'{method}: {response.text}')

print("\nPUT requests:")
for method in methods:
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data='{"method":"'+method+'"}')
    print(f'{method}: {response.text}')

print("\nDELETE requests:")
for method in methods:
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data='{"method":"'+method+'"}')
    print(f'{method}: {response.text}')