import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest
import random
import string


@allure.feature("Registration")
class TestUserRegister(BaseCase):

    missing_params = [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ]

    @allure.story("Create user")
    @allure.title("Test create user successfully")
    @allure.description("Check that it is possible to register user with email, password, username, firstName and "
                        "lastName")
    @allure.severity(severity_level="blocker")
    def test_create_user_successfully(self):
        with allure.step("Prepare user data: email, password, username, firstName and lastName"):
            data = self.prepare_registration_data()

        with allure.step("Register user"):
            response = MyRequests.post("/user/", data=data)

        with allure.step("Check that status code is 200 and id of the user is returned in the response"):
            Assertions.assert_status_code(response, 200)
            Assertions.assert_json_has_key(response, "id")

    @allure.story("Unsuccessful user creation")
    @allure.title("Test create user with existing email")
    @allure.description("Check that it is not possible to create a new user with an existing email")
    @allure.severity(severity_level="blocker")
    def test_create_user_with_existing_email(self):
        with allure.step("Prepare user data: existing email and new password, username, firstName and lastName"):
            email = 'vinkotov@example.com'
            data = self.prepare_registration_data(email)

        with allure.step("Try to register user"):
            response = MyRequests.post("/user/", data=data)

        with allure.step("Check that status code is 400 and error is returned in the response"):
            Assertions.assert_status_code(response, 400)
            Assertions.assert_response_content(response, f"Users with email '{email}' already exists")

    @allure.story("Unsuccessful user creation")
    @allure.title("Test create user with incorrect email")
    @allure.description("Check that it is not possible to create a new user with an email w/o @ sign")
    @allure.severity(severity_level="normal")
    def test_create_user_email_has_no_at_sign(self):
        with allure.step("Prepare user data: bad email w/o @ and password, username, firstName and lastName"):
            bad_email = 'learn_qaexample.com'
            data = self.prepare_registration_data(bad_email)

        with allure.step("Try to register user"):
            response = MyRequests.post("/user/", data=data)

        with allure.step("Check that status code is 400 and error is returned in the response"):
            Assertions.assert_status_code(response, 400)
            Assertions.assert_response_content(response, "Invalid email format")

    @allure.story("Unsuccessful user creation")
    @allure.title("Test create user with one missing parameter")
    @allure.description("Check that it is not possible to create a new user if one of the parameters is missing")
    @allure.severity(severity_level="normal")
    @pytest.mark.parametrize('param', missing_params)
    def test_create_user_without_one_param(self, param):
        with allure.step("Prepare user data w/o one of the parameters"):
            data = self.prepare_registration_data()
            del data[param]

        with allure.step("Try to register user"):
            response = MyRequests.post("/user/", data=data)

        with allure.step("Check that status code is 400 and error is returned in the response"):
            Assertions.assert_status_code(response, 400)
            Assertions.assert_response_content(response, f"The following required params are missed: {param}")

    @allure.story("Unsuccessful user creation")
    @allure.title("Test create user with too short firstName")
    @allure.description("Check that it is not possible to create a new user if length of the firstName = 1 char")
    @allure.severity(severity_level="normal")
    def test_create_user_with_short_firstname(self):
        with allure.step("Prepare user data with firstName = 1 char"):
            data = self.prepare_registration_data()
            data['firstName'] = 'I'

        with allure.step("Try to register user"):
            response = MyRequests.post("/user/", data=data)

        with allure.step("Check that status code is 400 and error is returned in the response"):
            Assertions.assert_status_code(response, 400)
            Assertions.assert_response_content(response, "The value of 'firstName' field is too short")

    @allure.story("Unsuccessful user creation")
    @allure.title("Test create user with too long firstName")
    @allure.description("Check that it is not possible to create a new user if length of the firstName > 250 symbols")
    @allure.severity(severity_level="normal")
    def test_create_user_with_too_long_firstname(self):
        with allure.step("Prepare user data with firstName > 250 symbols"):
            data = self.prepare_registration_data()
            data['firstName'] = ''.join(random.choices(string.ascii_lowercase, k=251))
            print(data['firstName'])

        with allure.step("Try to register user"):
            response = MyRequests.post("/user/", data=data)

        with allure.step("Check that status code is 400 and error is returned in the response"):
            Assertions.assert_status_code(response, 400)
            Assertions.assert_response_content(response, "The value of 'firstName' field is too long")

