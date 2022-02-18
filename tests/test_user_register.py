import allure
import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Register user cases")
class TestUserRegister(BaseCase):
    reg_fields = [
            "password",
            "username",
            "firstName",
            "lastName",
            "email",
    ]

    @allure.feature("Register")
    @allure.title("User registration")
    @allure.description("This test registers a user with a random email")
    @allure.step("Starting test test_create_user_successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.feature("Register")
    @allure.title("User registration with existing email")
    @allure.description("This test registers a user with a existing email")
    @allure.step("Starting test test_create_user_with_existing_email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.feature("Register")
    @allure.title("User registration with incorrect email")
    @allure.description("This test registers a user with a incorrect email")
    @allure.step("Starting test test_create_user_with_incorrect_email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_incorrect_email(self):
        email = 'risaevexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content {response.content}"

    @allure.feature("Register")
    @allure.title("User registration with out one field")
    @allure.description("This test registers a user with one field")
    @allure.step("Starting test test_create_user_with_out_one_field")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('field', reg_fields)
    def test_create_user_with_out_one_field(self, field):
        data = self.prepare_registration_data()
        data.pop(field)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {field}", f"Unexpected response content {response.content}"

    @allure.feature("Register")
    @allure.title("User registration with short name")
    @allure.description("This test registers a user with short name")
    @allure.step("Starting test test_create_user_with_short_name")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = "a"
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", f"Unexpected response content {response.content}"

    @allure.feature("Register")
    @allure.title("User registration with long name")
    @allure.description("This test registers a user with long name")
    @allure.step("Starting test test_create_user_with_long_name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = "7WEGfpDHawniF37ApVYum9dj1PkT7ICO7Mte7tSsffyuSxZlLuekBXORWne7NupjnUa1c35LgTh8eiaeh1XyoKsL" \
                            "9BmrEPyYGgkPIJd8XCKqgl1NNPpyOYfqx3D0qcljkubGIRSieG0GY6IC03fKmKJAcZk7HTY9HhTkVJ0q2RhBkmdt" \
                            "qPWzdEVBrNohL775GRcgYpTrlmnIgrXnHwCU99MXvjlSOwR0B8hXjqodcuJ0UNuy2ZJDpAqck6B"
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", f"Unexpected response content {response.content}"


