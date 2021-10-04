import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.feature('User deletion')
class TestUserDelete(BaseCase):
    super_user = {
        'email': 'vinkotov@example.com',
        'password': '1234'
    }
    super_user_id = '2'

    @allure.story("User deletion with specific IDs")
    @allure.title("Test deletion of the super user")
    @allure.description("This test checks the deletion of the user with ID=2")
    @allure.severity(severity_level="critical")
    def test_delete_super_user(self):
        with allure.step("Login as super user"):
            response = MyRequests.post("/user/login", data=self.super_user)

            Assertions.assert_json_has_key(response, "user_id")
            Assertions.assert_json_value_by_name(response, "user_id", int(self.super_user_id),
                                                 f"The value of 'user_id' is wrong. Expected {self.super_user_id}, "
                                                 f"but received {self.get_json_value(response, 'user_id')}")

            auth_sid = self.get_cookie(response, "auth_sid")
            token = self.get_header(response, "x-csrf-token")

        with allure.step("Try to delete super user"):
            del_response = MyRequests.delete(f"/user/{self.super_user_id}",
                                             headers={"x-csrf-token": token},
                                             cookies={"auth_sid": auth_sid})

            expected_error_message = 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'

            Assertions.assert_status_code(del_response, 400)
            Assertions.assert_response_content(del_response, expected_error_message)

    @allure.story("Successful user deletion")
    @allure.title("Test successful user deletion from service")
    @allure.description("Goal is to check that the authorized user can delete own data")
    @allure.severity(severity_level="blocker")
    def test_delete_user(self):
        with allure.step("Register new user"):
            user = self.prepare_registration_data()
            register_response = MyRequests.post("/user/", data=user)

            Assertions.assert_status_code(register_response, 200)
            Assertions.assert_json_has_key(register_response, "id")

            email = user['email']
            password = user['password']
            user_id = self.get_json_value(register_response, "id")

        with allure.step("Login as new user"):
            login_data = {
                'email': email,
                'password': password
            }
            login_response = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(login_response, "auth_sid")
            token = self.get_header(login_response, "x-csrf-token")

        with allure.step("User deletion by user id"):
            delete_response = MyRequests.delete(f"/user/{user_id}",
                                                headers={"x-csrf-token": token},
                                                cookies={"auth_sid": auth_sid})

            Assertions.assert_status_code(delete_response, 200)

        with allure.step("Authorized super user tries to get the data of the deleted user"):
            su_login_response = MyRequests.post("/user/login", data=self.super_user)

            Assertions.assert_json_has_key(su_login_response, "user_id")

            su_auth_sid = self.get_cookie(su_login_response, "auth_sid")
            su_token = self.get_header(su_login_response, "x-csrf-token")

            su_get_user_response = MyRequests.get(f"/user/{user_id}",
                                                  headers={"x-csrf-token": su_token},
                                                  cookies={"auth_sid": su_auth_sid}
                                                  )

            Assertions.assert_status_code(su_get_user_response, 404)
            Assertions.assert_response_content(su_get_user_response, "User not found")

        with allure.step("Try to login with data of the deleted user"):
            deleted_login_response = MyRequests.post("/user/login", data=login_data)

            Assertions.assert_status_code(deleted_login_response, 400)
            Assertions.assert_response_content(deleted_login_response, "Invalid username/password supplied")

    @allure.story("Deletion by other user")
    @allure.title("Test deletion of the user by other user")
    @allure.description("Goal is to check that the user can't delete other user")
    @allure.severity(severity_level="critical")
    def test_delete_user_as_other_user(self):
        with allure.step("Register User1 who tries to delete User2"):
            user1 = self.prepare_registration_data()
            register1_response = MyRequests.post("/user/", data=user1)

            Assertions.assert_status_code(register1_response, 200)
            Assertions.assert_json_has_key(register1_response, "id")

            email1 = user1['email']
            password1 = user1['password']

        with allure.step("Register User2"):
            user2 = self.prepare_registration_data()
            register2_response = MyRequests.post("/user/", data=user2)

            Assertions.assert_status_code(register2_response, 200)
            Assertions.assert_json_has_key(register2_response, "id")

            user2_id = self.get_json_value(register2_response, "id")
            email2 = user2['email']
            password2 = user2['password']
            username2 = user2['username']
            lastname2 = user2['lastName']
            firstname2 = user2['firstName']

        with allure.step("Login as User1"):
            login_data1 = {
                'email': email1,
                'password': password1
            }
            login_response1 = MyRequests.post("/user/login", data=login_data1)

            auth_sid1 = self.get_cookie(login_response1, "auth_sid")
            token1 = self.get_header(login_response1, "x-csrf-token")

        with allure.step("Login as User2"):
            login_data2 = {
                'email': email2,
                'password': password2
            }
            login_response2 = MyRequests.post("/user/login", data=login_data2)

            auth_sid2 = self.get_cookie(login_response2, "auth_sid")
            token2 = self.get_header(login_response2, "x-csrf-token")

        with allure.step("User1 tries to delete User2"):
            delete_response = MyRequests.delete(f"/user/{user2_id}",
                                                headers={"x-csrf-token": token1},
                                                cookies={"auth_sid": auth_sid1})

            Assertions.assert_status_code(delete_response, 200)

        with allure.step("User2 check his (or her) data"):
            get_data_response = MyRequests.get(f"/user/{user2_id}",
                                               headers={"x-csrf-token": token2},
                                               cookies={"auth_sid": auth_sid2}
                                               )
            expected_fields = ["username", "email", "firstName", "lastName"]

            Assertions.assert_status_code(get_data_response, 200)
            Assertions.assert_json_has_keys(get_data_response, expected_fields)
            Assertions.assert_json_value_by_name(get_data_response, expected_fields[0], username2,
                                                 f"Wrong {expected_fields[0]}! Expected {username2}, "
                                                 f"but received {self.get_json_value(get_data_response, expected_fields[0])}")
            Assertions.assert_json_value_by_name(get_data_response, expected_fields[1], email2,
                                                 f"Wrong {expected_fields[1]}! Expected {email2}, "
                                                 f"but received {self.get_json_value(get_data_response, expected_fields[1])}")
            Assertions.assert_json_value_by_name(get_data_response, expected_fields[2], firstname2,
                                                 f"Wrong {expected_fields[2]}! Expected {firstname2}, "
                                                 f"but received {self.get_json_value(get_data_response, expected_fields[2])}")
            Assertions.assert_json_value_by_name(get_data_response, expected_fields[3], lastname2,
                                                 f"Wrong {expected_fields[3]}! Expected {lastname2}, "
                                                 f"but received {self.get_json_value(get_data_response, expected_fields[3])}")
