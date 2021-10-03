from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        expected_fields = ["username", "email", "firstName", "lastName"]

        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_as_another_user(self):
        # Register User1 for auth who will get data of another User2
        user1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=user1)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user1_email = user1['email']
        user1_password = user1['password']
        user1_id = self.get_json_value(response1, "id")

        # Register User2 which data User1 will get
        user2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=user2)

        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        user2_username = user2['username']
        user2_id = self.get_json_value(response2, "id")

        # Login as User1
        login_data = {
            'email': user1_email,
            'password': user1_password
        }
        response3 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_json_has_key(response3, "user_id")
        Assertions.assert_json_value_by_name(response3, "user_id", int(user1_id),
                                             f"The value of 'user_id' is wrong. Expected {user1_id}, "
                                             f"but received {self.get_json_value(response3, 'user_id')}")

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # Get User2 data as authorized User1
        response4 = MyRequests.get(f"/user/{user2_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        Assertions.assert_json_has_key(response4, "username")
        Assertions.assert_json_value_by_name(response4, "username", user2_username,
                                             f"The username value of the user with id={user2_id} is wrong!"
                                             f"\nExpected: {user2_username}\n"
                                             f"Actual: {self.get_json_value(response4, 'username')}")

