import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):
    @allure.feature("Auth", "Delete")
    @allure.title("Delete non-deleted user")
    @allure.description("This test tries to delete a user that cannot be deleted")
    @allure.step("Starting test test_delete_non_deleted_user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_non_deleted_user(self):
        # LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        # DELETE
        response2 = MyRequests.delete(f"/user/{user_id_from_auth_method}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response2.content}"

    @allure.feature("Register", "Auth", "Delete", "Get")
    @allure.title("Delete just created user")
    @allure.description("This test registers a user and then deletes")
    @allure.step("Starting test test_delete_just_created_user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
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

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}")

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", f"Unexpected response content {response4.content}"

    @allure.feature("Register", "Auth", "Delete", "Get")
    @allure.title("Delete user auth as another user")
    @allure.description("This test logs in as one user and tries to delete another user")
    @allure.step("Starting test test_delete_user_auth_as_another_user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_auth_as_another_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        MyRequests.delete("/user/26010",
                          headers={"x-csrf-token": token},
                          cookies={"auth_sid": auth_sid}
                          )

        # GET
        response3 = MyRequests.get("/user/26010")

        assert response3.content.decode("utf-8") != "User not found", \
            f"Unexpected response content {response3.content}. The user was deleted, but should not have been"
