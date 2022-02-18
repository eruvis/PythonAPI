import json

import pytest
import requests


class TestHeaderMethodRequest:
    user_agent_and_expected_value = [
        [
            "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}
        ],
        [
            "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
            {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}
        ],
        [
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}
        ],
        [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
            {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}
        ],
        [
            "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}
        ]
    ]

    @pytest.mark.parametrize('data', user_agent_and_expected_value)
    def test_header_method_request(self, data):
        response = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers={"User-Agent": data[0]}
        )

        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        platform = "platform"
        browser = "browser"
        device = "device"

        assert platform in response_as_dict, f"Response JSON doesn't have key '{platform}'"
        assert browser in response_as_dict, f"Response JSON doesn't have key '{browser}'"
        assert device in response_as_dict, f"Response JSON doesn't have key '{device}'"

        assert response_as_dict[platform] == data[1][platform], f"Received 'platform' value is not what expected. " \
                                                                f"Received: '{response_as_dict[platform]}'. " \
                                                                f"Expected: '{data[1][platform]}'."
        assert response_as_dict[browser] == data[1][browser], f"Received 'browser' value is not what expected. " \
                                                              f"Received: '{response_as_dict[browser]}'. " \
                                                              f"Expected: '{data[1][browser]}'"
        assert response_as_dict[device] == data[1][device], f"Received 'device' value is not what expected. " \
                                                            f"Received: '{response_as_dict[device]}'. " \
                                                            f"Expected: '{data[1][device]}'"
