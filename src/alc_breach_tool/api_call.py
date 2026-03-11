import requests
import logging
import os
import time
#****
# was gonna use the intelx sdk but it returns mixed types when testing (dict vs int)this is messy for debugging and i wasnt gonna spend my time dealing 
# with that. Compared to just doing it myself and seeing the raw response and status code. This then led me to search for better APIs as IntelX free tier
# was super clunky with slow response times and low rate limiting shared with everyone who used the API due to the key being shared by everyone. I then settled
# on XPOSEDORNOT which is much better for this use case and allows me to just query the email instead of sending a POST then from that POST having to send a GET 
# to return the results. 
#****
logger = logging.getLogger("alc.core")


def api_call_xposedornot(email_list, config):
    """
    This method queries an external breach intelligence provider to determine
    whether an email address has appeared in known data breaches.
    """
    #loads api config from yaml
    search_url = config["api_url"]
    timeout = config["timeout_seconds"]
    max_retries = config["max_retries"]
    backoff_base = config["backoff_base_seconds"]

    #standard used for api calls 
    headers = {
        "User-Agent": "ALC Breach Tool - Email Reputation Checker (college project)",
        "Accept": "application/json",
    }

    results = []

    #iterate through each email address in the email_list
    for email in email_list:
        logger.info("Checking email: %s", email)
        url = search_url.format(email=email)

        result = {
            "email": email,
            "breached": None,
            "breaches": []
        }
        #retry loop for server errors and rate limiting 
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=timeout)

                logger.info(
                    "XposedOrNot response | email=%s | status=%s | attempt=%s",
                    email,
                    response.status_code,
                    attempt + 1
                )
                #handles 429 
                if response.status_code == 429:
                    logger.warning(
                        "Rate limited for %s on attempt %s",
                        email,
                        attempt + 1
                    )

                    if attempt < max_retries - 1:
                        time.sleep(backoff_base * (2 ** attempt))
                        continue

                    result["error"] = "Rate limit exceeded after retries"
                    break
                #handles 5xx errors 
                if 500 <= response.status_code < 600:
                    logger.warning(
                        "Server error for %s on attempt %s",
                        email,
                        attempt + 1
                    )

                    if attempt < max_retries - 1:
                        time.sleep(backoff_base * (2 ** attempt))
                        continue

                    result["error"] = f"Server error: {response.status_code}"
                    break

                json_data = response.json()

                #breach detected 
                if "breaches" in json_data:
                    result["breached"] = True
                    result["breaches"] = json_data["breaches"][0] if json_data["breaches"] else []
                    logger.info("Breach found for %s", email)
                    break
                
                #no breach found
                elif json_data.get("Error") == "Not found":
                    result["breached"] = False
                    logger.info("No breach found for %s", email)
                    break
                
                #execpected response
                else:
                    result["error"] = f"Unexpected response: {json_data}"
                    logger.warning("Unexpected response for %s: %s", email, json_data)
                    break

            #request error or network        
            except requests.exceptions.RequestException as error:
                logger.error(
                    "Request failed for %s on attempt %s: %s",
                    email,
                    attempt + 1,
                    error
                )

                if attempt < max_retries - 1:
                    time.sleep(backoff_base * (2 ** attempt))
                else:
                    result["error"] = str(error)

            except ValueError:
                logger.error("Invalid JSON returned for %s", email)
                result["error"] = "Response was not valid JSON"
                break

        results.append(result)

    return results