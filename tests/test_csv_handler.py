import csv
from alc_breach_tool.csv_handler import read_emails, write_emails

def test_read_emails_removes_blanks_and_duplicates(tmp_path):
    input_file = tmp_path / "email_list.csv"
    input_file.write_text(
        "email\n"
        "Example@example.com\n"
        "\n"
        "mike@test.com\n"
        "example@example.com\n"
        "ADMIN@test.com\n",
        encoding="utf-8"
    )

    result = read_emails(str(input_file))

    assert result == [
        "example@example.com",
        "mike@test.com",
        "admin@test.com",
    ]


def test_write_emails_writes_expected_csv(tmp_path):
    output_file = tmp_path / "output_result.csv"

    results = [
        {
            "email": "example@example.com",
            "breached": True,
            "breaches": ["Adobe", "Dropbox"]
        },
        {
            "email": "admin@test.com",
            "breached": False,
            "breaches": []
        },
    ]

    write_emails(str(output_file), results)

    with open(output_file, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    assert rows == [
        ["email_address", "breached", "site_where_breached"],
        ["example@example.com", "True", "Adobe;Dropbox"],
        ["admin@test.com", "False", ""],
    ]