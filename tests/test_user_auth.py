import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.feature('Authorization')
class TestUserAuth(BaseCase):
    exclude_params = [
        "no_cookie",
        "no_token"
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        with allure.step(f"Setup: user with email {data['email']} is logged in"):
            response1 = MyRequests.post("/user/login", data=data)
            self.auth_sid = self.get_cookie(response1, "auth_sid")
            self.token = self.get_header(response1, "x-csrf-token")
            self.user_id_auth_method = self.get_json_value(response1, "user_id")

    @allure.story("Successful user authorization")
    @allure.title("Test successful user authorization")
    @allure.description("This test successfully authorizes user by email and password")
    @allure.severity(severity_level="blocker")
    def test_auth_user(self):
        with allure.step("Get user id of the authorized user"):
            response2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token},
                cookies={"auth_sid": self.auth_sid}
            )

        with allure.step("Check that user id from auth method is equal to user id from check method"):
            Assertions.assert_json_value_by_name(
                response2,
                "user_id",
                self.user_id_auth_method,
                "User id from auth method is not equal to user id from check method"
            )

    @allure.story("Negative cases: user is not authorized")
    @allure.title("Test user authorization w/o sending auth cookie or token")
    @allure.severity(severity_level="critical")
    @allure.description("This test checks authorization status w/o sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == "no_cookie":
            with allure.step("Auth request is sent without cookie"):
                response2 = MyRequests.get(
                    "/user/auth",
                    headers={"x-csrf-token": self.token})
        else:
            with allure.step("Auth request is sent without header"):
                response2 = MyRequests.get(
                    "/user/auth",
                    cookies={"auth_sid": self.auth_sid})

        with allure.step(f"Check that user is not authorized with condition {condition}"):
            Assertions.assert_json_value_by_name(
                response2,
                "user_id",
                0,
                f"User is authorized with condition {condition}"
            )
