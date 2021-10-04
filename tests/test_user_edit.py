import allure

from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions
import string
import random


@allure.feature('User update')
class TestUserEdit(BaseCase):
    @allure.story("Successful user update")
    @allure.title("Test update of user (must be logged in as this user)")
    @allure.description("Goal is to check that the user can update own data (firstName)")
    @allure.severity(severity_level="blocker")
    def test_edit_just_created_user(self):
        with allure.step("Register new user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_status_code(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            first_name = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step("Login as new user"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("Updating user's firstName"):
            new_name = first_name + ''.join(random.choices(string.ascii_lowercase, k=5))

            response3 = MyRequests.put(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid},
                                       data={"firstName": new_name}
                                       )

            Assertions.assert_status_code(response3, 200)

        with allure.step("Check that firstName is changed"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid}
                                       )

            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                new_name,
                "Wrong name of the user after edit"
            )

    @allure.story("Unsuccessful user update")
    @allure.title("Test update of user (must not be logged in as this user)")
    @allure.description("Check that the data of the user can't be edited if the user is not authorized")
    @allure.severity(severity_level="critical")
    def test_edit_user_not_auth(self):
        with allure.step("Create user for edit"):
            user = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=user)

            Assertions.assert_status_code(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            user_id = self.get_json_value(response1, "id")
            user_lastname = user['lastName']
            user_email = user['email']
            password = user['password']

        with allure.step("Login as user"):
            login_data = {
                'email': user_email,
                'password': password
            }

            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("Try to edit lastName of the user w/o sending auth cookies and headers"):
            new_lastname = user_lastname + ''.join(random.choices(string.ascii_lowercase, k=5))
            response3 = MyRequests.put(f"/user/{user_id}", data={"firstName": new_lastname})

            Assertions.assert_status_code(response3, 400)
            Assertions.assert_response_content(response3, "Auth token not supplied")

        with allure.step("Get user to check that lastName hasn't been changed"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid}
                                       )

            Assertions.assert_json_value_by_name(
                response4,
                "lastName",
                user_lastname,
                "Wrong name of the user after edit without authorization"
            )

    @allure.story("Unsuccessful user update")
    @allure.title("Test update email to incorrect value")
    @allure.description("Check that the email of the user can't be changed to the value w/o @ sign")
    @allure.severity(severity_level="normal")
    def test_edit_email_without_at_sign(self):
        with allure.step("Register user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_status_code(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step("Login as user"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("Edit user - change email to wrong email w/o @"):
            bad_email = 'learnqaexample.com'

            response3 = MyRequests.put(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid},
                                       data={"email": bad_email}
                                       )

            Assertions.assert_status_code(response3, 400)
            Assertions.assert_response_content(response3, "Invalid email format")

        with allure.step("Get user's data: email mustn't be changed"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid}
                                       )

            Assertions.assert_json_value_by_name(
                response4,
                "email",
                email,
                "Wrong email of the user after edit"
            )

    @allure.story("Unsuccessful user update")
    @allure.title("Test update firstName to incorrect value")
    @allure.description("Check that the firstName of the user can't be changed to the value with length=1")
    @allure.severity(severity_level="normal")
    def test_edit_firstname_too_short(self):
        with allure.step("Register user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_status_code(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            password = register_data['password']
            first_name = register_data['firstName']
            user_id = self.get_json_value(response1, "id")

        with allure.step("Login as user"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("Edit user - firstName length is 1 char"):
            bad_firstname = 'a'

            response3 = MyRequests.put(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid},
                                       data={"firstName": bad_firstname}
                                       )

            expected_error = 'Too short value for field firstName'
            Assertions.assert_status_code(response3, 400)
            Assertions.assert_json_has_key(response3, "error")
            Assertions.assert_json_value_by_name(response3, "error", expected_error,
                                                 f"Wrong error message!\nExpected: {expected_error}"
                                                 f"\nActual: {self.get_json_value(response3, 'error')}")

        with allure.step("Get user's data: firstName mustn't be changed"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid}
                                       )

            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                first_name,
                "Wrong firstName of the user after edit"
            )

    @allure.story("Unsuccessful user update")
    @allure.title("Test update user's data as another user")
    @allure.description("Check that authorized User1 can't change the data of User2")
    @allure.severity(severity_level="critical")
    def test_edit_user_as_another_user(self):
        with allure.step("Register User1 for auth who will edit data of User2"):
            user1 = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=user1)

            Assertions.assert_status_code(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            user1_email = user1['email']
            user1_password = user1['password']
            user1_id = self.get_json_value(response1, "id")

        with allure.step("Register User2 which data User1 will edit"):
            user2 = self.prepare_registration_data()
            response2 = MyRequests.post("/user/", data=user2)

            Assertions.assert_status_code(response2, 200)
            Assertions.assert_json_has_key(response2, "id")

            user2_password = user2['password']
            user2_email = user2['email']
            user2_username = user2['username']
            user2_id = self.get_json_value(response2, "id")

        with allure.step("Login as User1"):
            login_data_user1 = {
                'email': user1_email,
                'password': user1_password
            }
            response3 = MyRequests.post("/user/login", data=login_data_user1)

            Assertions.assert_json_has_key(response3, "user_id")
            Assertions.assert_json_value_by_name(response3, "user_id", int(user1_id),
                                                 f"The value of 'user_id' is wrong. Expected {user1_id}, "
                                                 f"but received {self.get_json_value(response3, 'user_id')}")

            auth_sid_user1 = self.get_cookie(response3, "auth_sid")
            token_user1 = self.get_header(response3, "x-csrf-token")

        with allure.step("Edit User2 as User1 - try to change the username"):
            new_username = 'BadUser' + ''.join(random.choices(string.digits, k=4))

            response4 = MyRequests.put(f"/user/{user2_id}",
                                       headers={"x-csrf-token": token_user1},
                                       cookies={"auth_sid": auth_sid_user1},
                                       data={"username": new_username}
                                       )

            Assertions.assert_status_code(response4, 200)

        with allure.step("Login as User2"):
            login_data_user2 = {
                'email': user2_email,
                'password': user2_password
            }
            response5 = MyRequests.post("/user/login", data=login_data_user2)

            Assertions.assert_json_has_key(response5, "user_id")
            Assertions.assert_json_value_by_name(response5, "user_id", int(user2_id),
                                                 f"The value of 'user_id' is wrong. Expected {user2_id}, "
                                                 f"but received {self.get_json_value(response5, 'user_id')}")

            auth_sid_user2 = self.get_cookie(response5, "auth_sid")
            token_user2 = self.get_header(response5, "x-csrf-token")

        with allure.step("Get User2 details to check the username"):
            response6 = MyRequests.get(f"/user/{user2_id}",
                                       headers={"x-csrf-token": token_user2},
                                       cookies={"auth_sid": auth_sid_user2}
                                       )

            Assertions.assert_json_value_by_name(
                response6,
                "username",
                user2_username,
                "Wrong firstName of the user after edit"
            )
