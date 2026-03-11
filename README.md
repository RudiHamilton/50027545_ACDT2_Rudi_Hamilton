# ALC Breach Assessment Tool

## Overview

This project implements a breach assesment tool for Antrim Logistics Company.
The application checks email addresses given in the CSV against a publicly avaliable breach API to identify potential breaches.

The tool reads email addresses from a CSV file, queries a breach intelligence provider, and generates structured outputs for analysts and management.

## Features

- CSV email ingestion
- Email validation and duplicate filtering
- Breach intelligence lookup via API
- Retry and backoff handling for API rate limits
- Structured CSV output for analysts
- Logging of API requests and processing steps
- Unit tests for core functionality

## Project Structure
.
├── config.yaml
├── requirements.txt
├── pytest.ini
├── README.md
├── report.md
├── .env
│
├── data/
│   ├── email_list.csv
│   └── output_result.csv
│
├── logs/
│   └── app.log
│
├── src/
│   └── alc_breach_tool/
│       ├── main.py
│       ├── api_call.py
│       ├── csv_handler.py
│       ├── config_loader.py
│       └── logging_config.py
│
└── tests/

## Installation

Clone the repository and install dependencies:

Unix:
    bash
        python -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt

Windows:
    bash
        .venv\Scripts\activate

## Configuration

Runtime configuration is stored in `config.yaml`.

Example settings include:

- API endpoint
- request timeout
- retry limits
- input and output file locations

## Running the Tool

Ensure the input CSV exists:
    data/email_list.csv

Run the application:
    bash
        python -m alc_breach_tool.main

## Example input

email
example@example.com
admin@test.com

## Example output

email_address,breached,site_where_breached
example@example.com,True,Adobe;Dropbox
admin@test.com,False,

## Architecture Diagram
```
                +----------------------+
                |    config.yaml       |
                |   .env / API key     |
                +----------------------+
                           |
                           v
+-------------+   +--------------------+   +----------------------+
| email_list  |-->|      main.py       |-->|  logging_config.py   |
|    .csv     |   | controls workflow  |   |  logs INFO / ERROR   |
+-------------+   +--------------------+   +----------------------+
                           |
                           v
                  +------------------+
                  |  csv_handler.py   |
                  | reads email list  |
                  +------------------+
                           |
                           v
                  +------------------+
                  |   api_call.py    |
                  | checks each email|
                  | against API      |
                  +------------------+
                           |
                           v
                  +------------------+
                  |   reporting.py   |
                  | metrics/summary  |
                  +------------------+
                       |         |
                       |         |
                       v         v
          +----------------+   +-------------+
          |output_result.csv|   |  report.md  |
          +----------------+   +-------------+
```
## Limitations

- The tool currently checks only email addresses.
- Results depend on the coverage of the external breach intelligence API.
- Free-tier APIs may impose rate limits.
- Using an .env file with no secrets (does not require secrets as free API but supports the use of a different API due to yaml)

## Testing

Unit tests are implemented using pytest.

Run tests with:

    bash
        pytest

## CI Pipeline 

CI pipeline exists and works and will fail if the tests do not pass checked this with github actions. 
