import logging
from dotenv import load_dotenv
from pathlib import Path
from alc_breach_tool.logging_config import setup_logging
from alc_breach_tool.csv_handler import read_emails, write_emails
from alc_breach_tool.api_call import api_call_xposedornot
from alc_breach_tool.config_loader import load_config
from alc_breach_tool.reporting import build_summary

#used to initialise the dotenv method and point to my env file 
load_dotenv()

#loads yaml
config = load_config()


def main():
    """
    Main function to setup the breach checking process:
    1. Initializes logging
    2. Loads configuration from YAML
    3. Reads email addresses from input CSV
    4. Calls breach intelligence API to check each email
    5. Writes results to output CSV
    6. Builds a markdown summary report
    """
    #initialise logging
    setup_logging()

    logger = logging.getLogger("alc.core")
    logger.info("Application started")

    #load input and output paths from config
    input_path = config["input_csv"]
    output_path = config["output_csv"]
    
    #reads emails from csv and returns a list of unique emaills
    email_list = read_emails(input_path)

    #calls api to check emails
    api_results = api_call_xposedornot(email_list, config)

    #writes results to csv
    write_emails(output_path, api_results)

    #builds markdown analyst report
    summary = build_summary(api_results)

    with open("report.md", "w", encoding="utf-8") as file:
        file.write(summary)
        
if __name__ == "__main__":
    main()