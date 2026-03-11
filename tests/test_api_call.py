from unittest.mock import Mock, patch
import requests
from alc_breach_tool.api_call import api_call_xposedornot


def test_api_call_xposedornot_breached():
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "breaches": [["Adobe", "Dropbox"]]
    }

    with patch("alc_breach_tool.api_call.requests.get", return_value=fake_response):
        result = api_call_xposedornot(["example@example.com"])

    assert result == [
        {
            "email": "example@example.com",
            "breached": True,
            "breaches": ["Adobe", "Dropbox"]
        }
    ]


def test_api_call_xposedornot_not_breached():
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "Error": "Not found"
    }

    with patch("alc_breach_tool.api_call.requests.get", return_value=fake_response):
        result = api_call_xposedornot(["admin@test.com"])

    assert result == [
        {
            "email": "admin@test.com",
            "breached": False,
            "breaches": []
        }
    ]


def test_api_call_xposedornot_timeout():
    with patch(
        "alc_breach_tool.api_call.requests.get",
        side_effect=requests.exceptions.Timeout
    ):
        result = api_call_xposedornot(["example@example.com"])

    assert result == [
        {
            "email": "example@example.com",
            "breached": None,
            "breaches": [],
            "error": ""
        }
    ]

def test_api_call_xposedornot_retries_after_429():
    first_response = Mock()
    first_response.status_code = 429

    second_response = Mock()
    second_response.status_code = 200
    second_response.json.return_value = {
        "Error": "Not found"
    }

    with patch(
        "alc_breach_tool.api_call.requests.get",
        side_effect=[first_response, second_response]
    ), patch("alc_breach_tool.api_call.time.sleep") as mock_sleep:
        result = api_call_xposedornot(["admin@test.com"])

    assert result == [
        {
            "email": "admin@test.com",
            "breached": False,
            "breaches": []
        }
    ]
    mock_sleep.assert_called_once_with(1)