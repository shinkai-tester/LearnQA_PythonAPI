from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest
import random
import string


class TestUserRegister(BaseCase):

    missing_params = [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, f"Users with email '{email}' already exists")

    def test_create_user_email_has_no_at_sign(self):
        bad_email = 'learn_qaexample.com'
        data = self.prepare_registration_data(bad_email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "Invalid email format")

    @pytest.mark.parametrize('param', missing_params)
    def test_create_user_without_one_param(self, param):
        data = self.prepare_registration_data()
        del data[param]

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, f"The following required params are missed: {param}")

    def test_create_user_with_short_firstname(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'I'

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "The value of 'firstName' field is too short")

    def test_create_user_with_too_long_firstname(self):
        data = self.prepare_registration_data()
        data['firstName'] = ''.join(random.choices(string.ascii_lowercase, k=251))

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "The value of 'firstName' field is too long")

