from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions
import string
import random


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
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

        # EDIT USER

        new_name = first_name + ''.join(random.choices(string.ascii_lowercase, k=5))

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )

        Assertions.assert_status_code(response3, 200)

        # GET USER'S DATA
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

    def test_edit_user_not_auth(self):
        # Create User for edit
        user = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=user)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        user_lastname = user['lastName']
        user_email = user['email']
        password = user['password']

        # Login as User
        login_data = {
            'email': user_email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Try to edit the lastName of the User
        new_lastname = user_lastname + ''.join(random.choices(string.ascii_lowercase, k=5))
        response3 = MyRequests.put(f"/user/{user_id}", data={"firstName": new_lastname})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_response_content(response3, "Auth token not supplied")

        # Get the User to check that lastName hasn't been changed
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

    def test_edit_email_without_at_sign(self):
        # Register User
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit User - change email to wrong email w/o @

        bad_email = 'learnqaexample.com'

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": bad_email}
                                   )

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_response_content(response3, "Invalid email format")

        # Get User's data
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

    def test_edit_firstname_too_short(self):
        # Register User
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        first_name = register_data['firstName']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit User - firstName length is 1 char

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

        # Get User's data
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

    def test_edit_user_as_another_user(self):
        # Register User1 for auth who will edit data of another User2
        user1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=user1)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user1_email = user1['email']
        user1_password = user1['password']
        user1_id = self.get_json_value(response1, "id")

        # Register User2 which data User1 will edit
        user2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=user2)

        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        user2_password = user2['password']
        user2_email = user2['email']
        user2_username = user2['username']
        user2_id = self.get_json_value(response2, "id")

        # Login as User1
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

        # Edit User2 as User1 - try to change the password

        new_username = 'BadUser' + ''.join(random.choices(string.digits, k=4))

        response4 = MyRequests.put(f"/user/{user2_id}",
                                   headers={"x-csrf-token": token_user1},
                                   cookies={"auth_sid": auth_sid_user1},
                                   data={"username": new_username}
                                   )

        Assertions.assert_status_code(response4, 200)

        # Login as User2
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

        # Get User2 details
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
