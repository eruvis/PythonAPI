import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Edit user cases")
class TestUserEdit(BaseCase):
    @allure.feature("Register", "Auth", "Edit", "Get")
    @allure.title("Edit just created user")
    @allure.description("This test registers a user and then edits")
    @allure.step("Starting test test_edit_just_created_user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        last_name = register_data['lastName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.feature("Edit")
    @allure.title("Edit user without authorization")
    @allure.description("This test tries to make changes to user data without authorization")
    @allure.step("Starting test test_edit_user_without_authorization")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_user_without_authorization(self):
        new_name = "Changed Name"

        response = MyRequests.put(f"/user/26013", data={"firstName": new_name})

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == "Auth token not supplied", f"Unexpected response content {response.content}"

    @allure.feature("Auth", "Edit", "Get")
    @allure.title("Edit user auth as another user")
    @allure.description("This test logs in as one user and tries to edit another user")
    @allure.step("Starting test test_edit_user_auth_as_another_user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_user_auth_as_another_user(self):
        # LOGIN
        # ID 26029
        data = {
            'email': 'risaev@yahoo.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # EDIT
        new_username = "sparta"

        MyRequests.put(f"/user/26000",
                       headers={"x-csrf-token": token},
                       cookies={"auth_sid": auth_sid},
                       data={"firstName": new_username}
                       )

        # GET
        response3 = MyRequests.get("/user/26000")

        Assertions.assert_json_not_value_by_name(
            response3,
            "username", 
            new_username,
            "The username has changed. What shouldn't have been"
        )

    @allure.feature("Auth", "Edit")
    @allure.title("Edit user email")
    @allure.description("This test edit user email to email without @")
    @allure.step("Starting test test_edit_user_email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_user_email(self):
        # LOGIN
        data = {
            'email': 'risaev@yahoo.com',
            'password': '1234'
        }
        user_id = 26029

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # EDIT
        new_email = (data['email']).replace('@', '')

        response2 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email}
                                   )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            "utf-8") == f"Invalid email format", f"Unexpected response content {response2.content}"

    @allure.feature("Auth", "Edit")
    @allure.title("Edit user name")
    @allure.description("This test edit user name to short name")
    @allure.step("Starting test test_edit_user_name")
    @allure.severity(allure.severity_level.MINOR)
    def test_edit_user_name(self):
        # LOGIN
        data = {
            'email': 'risaev@yahoo.com',
            'password': '1234'
        }
        user_id = 26029

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # EDIT
        new_name = "a"

        response2 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(
            response2,
            "error",
            "Too short value for field firstName",
            f"Unexpected response content {response2.content}"
        )
