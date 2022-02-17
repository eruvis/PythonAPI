import requests


class TestHeaderMethodRequest:
    def test_header_method_request(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        assert "x-secret-homework-header" in response.headers, "There is no 'x-secret-homework-header' headers in the response"
        assert response.headers["x-secret-homework-header"] == "Some secret value", "x-secret-homework-header header value does not match 'Some secret value'"
