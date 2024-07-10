from unittest.mock import patch
from datetime import datetime
from services.timestamp_service import TimestampService


def test_apply_timestamp_to_new_document():
    test_dict = {"foo": "bar"}
    fixed_datetime = datetime(2024, 4, 29, 12, 0, 0)

    with patch("services.timestamp_service.datetime") as mocked_datetime:
        mocked_datetime.now.return_value = fixed_datetime

        TimestampService.apply_timestamp_to_document(test_dict)

    assert test_dict["date_created"] == fixed_datetime


def test_apply_timestamp_to_document_exception(capsys):
    test_dict = {"foo": "bar"}

    with patch("services.timestamp_service.datetime") as mocked_datetime:
        mocked_datetime.now.side_effect = Exception("Datetime error")

        TimestampService.apply_timestamp_to_document(test_dict)

    assert "date_created" not in test_dict
    assert (
        "An error occurred while applying timestamp to document"
        in capsys.readouterr().out
    )
