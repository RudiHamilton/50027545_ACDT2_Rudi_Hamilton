import csv
import logging
import re

logger = logging.getLogger("alc.core")

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

#ensures email is valid format
def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email))

#reads emails from csv and returns a list of unique emails. 
def read_emails(inputpath: str) -> list[str]:
    """
    Reads a CSV file containing email addresses and returns
    a list of validated, unique emails.
    """

    emails = []
    seen = set()

    with open(inputpath, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row["email"].strip().lower()

            #skip blanks
            if not email:
                continue

            #skip duplicates
            if email in seen:
                logger.info(f"Duplicate email skipped: {email}")
                continue

            #skip invalid emails
            if not is_valid_email(email):
                logger.error("Invalid email skipped: %s", email)
                continue

            seen.add(email)
            emails.append(email)
            #logs the email thats loaded as if the csv is being uploaded by user it wont be a secret. Can change this out of loop to be a simple statement
            logger.info(f"Loaded email: {email}")

    return emails

#writes emails recieved from api to csv 
def write_emails(outputpath: str, results: list[dict]) -> None:
    """
    Recieves a dict of results from the api call and writes them to a csv file. The csv file will have the following columns:
    - email_address: the email address that was checked
    - breached: whether the email address was found in a breach (True or False)
    - site_where_breached: a semicolon-separated list of sites where the email was found
    """
    with open(outputpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["email_address", "breached", "site_where_breached"])

        for result in results:
            email = result["email"]
            breached = result["breached"]
            sites = result["breaches"]

            writer.writerow([
                    email,
                    bool(breached),
                    ";".join(sites)
                ])

            logger.info(f"Wrote email to csv: {email}")
