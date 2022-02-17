import requests


class TestCookieMethodRequest:
    def test_cookie_method_request(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        assert "HomeWork" in response.cookies, "There is no HomeWork cookie in the response"
        assert response.cookies["HomeWork"] == "hw_value", "HomeWork cookie value does not match hw_value"
