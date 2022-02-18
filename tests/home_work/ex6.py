import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
print(f"Redirects: {response.history}")
amount_redirects = len(response.history)
print(f"Amount of redirects: {amount_redirects}")
print(f"Final URL: {response.history[amount_redirects-1].url }")