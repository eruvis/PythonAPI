import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    reg_fields = [
            "password",
            "username",
            "firstName",
            "lastName",
            "email",
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'risaevexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('field', reg_fields)
    def test_create_user_with_out_one_field(self, field):
        data = self.prepare_registration_data()
        data.pop(field)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {field}", f"Unexpected response content {response.content}"

    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = "a"
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", f"Unexpected response content {response.content}"

    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = "7WEGfpDHawniF37ApVYum9dj1PkT7ICO7Mte7tSsffyuSxZlLuekBXORWne7NupjnUa1c35LgTh8eiaeh1XyoKsL" \
                            "9BmrEPyYGgkPIJd8XCKqgl1NNPpyOYfqx3D0qcljkubGIRSieG0GY6IC03fKmKJAcZk7HTY9HhTkVJ0q2RhBkmdt" \
                            "qPWzdEVBrNohL775GRcgYpTrlmnIgrXnHwCU99MXvjlSOwR0B8hXjqodcuJ0UNuy2ZJDpAqck6B"
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", f"Unexpected response content {response.content}"


