import os
from datetime import datetime
import logging
from dotenv import load_dotenv
from bsky_api import login, DID_resolve
from markov_gen import generate, refresh_dataset, get_account_posts
from time_utils import calculate_refresh_interval, calculate_next_refresh, sleep_until_next_refresh
from markovchain.text import MarkovText

# Ensure the log directory exists
log_directory = 'log'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up logging to a file in the log directory
logging.basicConfig(
    filename=os.path.join(log_directory, 'general.log'), 
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("NEW EXECUTION OF APPLICATION\n\n\n")

# Load environment variables
load_dotenv()

source_handle = os.getenv("SOURCE_HANDLE")
destination_handle = os.getenv("DESTINATION_HANDLE")
char_limit = int(os.getenv("CHAR_LIMIT", 280))

# Log environment variable loading
logging.debug("Loaded environment variables: SOURCE_HANDLE=%s, DESTINATION_HANDLE=%s, CHAR_LIMIT=%d",
              source_handle, destination_handle, char_limit)

# Login to source client and resolve DID
try:
    source_client = login("SOURCE_HANDLE", "SRC_APP_PASS")
    logging.info("Successfully logged in to source account.")
    
    source_did_package = DID_resolve(source_handle)
    source_did = source_did_package['did']
    logging.info("Resolved source DID: %s", source_did)

    destination_client = login("DESTINATION_HANDLE", "DST_APP_PASS")
    logging.info("Successfully logged in to destination account.")

except Exception as e:
    logging.exception("An error occurred during setup: %s", e)
    quit(1)

markov = MarkovText()

def generate_and_post_example():
    global markov, char_limit, destination_client

    generated_text = ' '.join(generate(markov, char_limit))
    logging.debug("Generated text for post: %s", generated_text)

    try:
        response = destination_client.send_post(
            text=generated_text,
            langs=['en']
        )
        post_link = response['uri']
        logging.info("Posted to destination Bluesky account successfully: %s", post_link)
    except Exception as e:
        logging.error("Error posting to destination Bluesky account: %s", e)

try:
    while True:
        current_time = datetime.now()
        refresh_interval = calculate_refresh_interval()
        next_refresh = calculate_next_refresh(current_time, refresh_interval)

        logging.debug("Current time: %s, Refresh interval: %s, Next refresh: %s", current_time, refresh_interval, next_refresh)

        source_posts = get_account_posts(source_client, source_did)
        logging.debug("Fetched source posts for DID: %s", source_did)

        markov = refresh_dataset(markov, source_posts)
        logging.info("Markov dataset refreshed.")

        generate_and_post_example()
        sleep_until_next_refresh(next_refresh)

except KeyboardInterrupt:
    logging.info("Exiting on user interrupt.")