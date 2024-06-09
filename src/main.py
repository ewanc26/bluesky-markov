import os
import time
from datetime import datetime
import dotenv
from bsky_api import login, DID_resolve
from markov_gen import generate, refresh_dataset, get_account_posts
from time_utils import calculate_refresh_interval, calculate_next_refresh, sleep_until_next_refresh
from markovchain.text import MarkovText

dotenv.load_dotenv()

source_handle = os.getenv("SOURCE_HANDLE")
destination_handle = os.getenv("DESTINATION_HANDLE")
char_limit = int(os.getenv("CHAR_LIMIT", 280))

source_client = login("SOURCE_HANDLE", "SRC_APP_PASS")
source_did_package = DID_resolve(source_handle)
source_did = source_did_package['did']

destination_client = login("DESTINATION_HANDLE", "DST_APP_PASS")

markov = MarkovText()

def generate_and_post_example():
    global markov, char_limit, destination_client

    generated_text = ' '.join(generate(markov, char_limit))

    print("Generated Text for Post:", generated_text)

    try:
        response = destination_client.send_post(
            text=generated_text,
            visibility="public"
        )
        post_link = response['uri']
        print(f"Posted to destination Bluesky account successfully: {post_link}")
    except Exception as e:
        print(f"Error posting to destination Bluesky account: {e}")

try:
    while True:
        current_time = datetime.now()
        refresh_interval = calculate_refresh_interval()
        next_refresh = calculate_next_refresh(current_time, refresh_interval)

        source_posts = get_account_posts(source_client, source_did)
        markov = refresh_dataset(markov, source_posts)
        generate_and_post_example()

        sleep_until_next_refresh(next_refresh)

except KeyboardInterrupt:
    print("\nExiting...")
