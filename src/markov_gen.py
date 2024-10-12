import logging
import os
from markovchain.text import MarkovText
from clean import clean_content  # Assuming clean_content is in clean.py

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

def retrieve_posts(client, client_did):
    post_list = []
    has_more = True
    cursor = None  # Initialise cursor for pagination

    logging.info(f"Starting to retrieve posts for client ID: {client_did}")

    while has_more:
        try:
            # Use cursor for pagination
            if cursor:
                data = client.app.bsky.feed.post.list(client_did, limit=100, cursor=cursor)
            else:
                data = client.app.bsky.feed.post.list(client_did, limit=100)

            logging.debug(f"Fetched data with cursor: {cursor}")

            # Log the structure of the returned data
            logging.debug("Data response structure: %s", data)

            # Check for the correct attribute containing the posts
            if not hasattr(data, 'records') or not data.records:
                logging.info("No more posts found or 'records' attribute is missing.")
                break

            # Fetch posts from the 'records' attribute
            posts = data.records

            # Add the posts to the post_list
            post_list.extend(posts.values())  # Access values directly from the dictionary

            logging.info(f"Retrieved {len(posts)} posts.")

            # Get the next cursor for pagination
            cursor = data.cursor  # Use the 'cursor' returned from the data for the next page
            has_more = bool(cursor)  # Continue if there is a next_cursor

        except Exception as e:
            logging.error(f"Error fetching posts: {e}")
            break

    logging.info(f"Completed retrieval of posts for client ID: {client_did}. Total posts retrieved: {len(post_list)}")

    # Log the structure of the first few posts for debugging
    for post in post_list[:5]:  # Show only the first 5 posts for brevity
        logging.debug("Post structure: %s", post)

    return post_list

def refresh_dataset(markov, source_posts):
    if not markov:
        markov = MarkovText()  # Initialise if not passed as an argument

    if source_posts:
        logging.info(f"Fetched {len(source_posts)} original posts and replies from the source account.")

    for post in source_posts:
        if isinstance(post, str):
            markov.data(post, part=True)  # Directly add the string if it's a simple string
        elif hasattr(post, 'text'):
            markov.data(post.text, part=True)  # Add if it's an object with text
        elif hasattr(post, 'value') and hasattr(post.value, 'text'):
            markov.data(post.value.text, part=True)  # Access text correctly
        else:
            logging.warning("Post does not have 'text' attribute, skipping: %s", post)

    markov.data('', part=False)  # Ensuring a proper closure of data input

    # Log the current dataset state for debugging
    logging.debug("Current length of posts: %s\n\n\n", len(source_posts))
    logging.debug("Current Markov dataset: %s", markov.storage)

    return markov

def generate(markov, char_limit):
    try:
        generated_text = markov()
    except KeyError as e:
        logging.error("KeyError occurred during generation: %s", e)
        return []

    if len(generated_text) > char_limit:
        generated_text = generated_text[:char_limit]

    logging.debug("Generated Text: %s", generated_text)

    words = generated_text.split()
    return words

def get_account_posts(client, client_did):
    posts = retrieve_posts(client, client_did)

    # Debugging: Print structure of the first post
    if posts:
        logging.debug("First post structure: %s", posts[0])

    # Ensure we are accessing the text correctly
    cleaned_posts = []
    for post in posts:
        if hasattr(post, 'value') and hasattr(post.value, 'text'):
            cleaned_text = clean_content(post.value.text)
            cleaned_posts.append(cleaned_text)
        elif hasattr(post, 'text'):  # Fall back to checking for a direct 'text' attribute
            cleaned_text = clean_content(post.text)
            cleaned_posts.append(cleaned_text)
        else:
            logging.warning("Post does not have 'value' or 'text', skipping: %s", post)

    return cleaned_posts