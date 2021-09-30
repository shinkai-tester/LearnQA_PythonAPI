import pytest
import requests


class TestUserAgent:
    dataprovider = [
        {
            "user_agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) "
                          "AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "platform": "Mobile",
            "browser": "No",
            "device": "Android"
        },
        {
            "user_agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) "
                          "AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
            "platform": "Mobile",
            "browser": "Chrome",
            "device": "iOS"
        },
        {
            "user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "platform": "Googlebot",
            "browser": "Unknown",
            "device": "Unknown"
        },
        {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
            "platform": "Web",
            "browser": "Chrome",
            "device": "No"
        },
        {
            "user_agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) "
                          "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "platform": "Mobile",
            "browser": "No",
            "device": "iPhone"
        }
    ]

    @pytest.mark.parametrize('data', dataprovider)
    def test_user_agent(self, data):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        user_agent = data["user_agent"]
        expected_platform = data["platform"]
        expected_browser = data["browser"]
        expected_device = data["device"]

        response = requests.get(url, headers={"User-Agent": user_agent})
        response_dict = response.json()

        assert response.status_code == 200, "Wrong response code"

        assert "user_agent" in response_dict, f"There is no field 'user_agent' in the response " \
                                              f"for the requested User Agent = '{data['useragent']}'"
        assert "platform" in response_dict, f"There is no field 'platform' in the response " \
                                            f"for the requested User Agent = '{data['useragent']}'"
        assert "browser" in response_dict, f"There is no field 'browser' in the response " \
                                           f"for the requested User Agent = '{data['useragent']}'"
        assert "device" in response_dict, f"There is no field 'device' in the response " \
                                          f"for the requested User Agent = '{data['useragent']}'"

        actual_platform = response_dict["platform"]
        actual_browser = response_dict["browser"]
        actual_device = response_dict["device"]

        assert actual_platform == expected_platform, \
            f"The platform with value = '{response_dict['platform']}' " \
            f"is not equal to the expected value = '{data['platform']}'"
        assert actual_browser == expected_browser, \
            f"The browser with value = '{response_dict['browser']}' " \
            f"is not equal to the expected value = '{data['browser']}'"
        assert actual_device == expected_device, \
            f"The device with value = '{response_dict['device']}' " \
            f"is not equal to the expected value = '{data['device']}'"
