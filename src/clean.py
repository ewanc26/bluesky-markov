from html import unescape
import re
import logging
import os

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

def clean_content(content):
    logging.debug("Original content: %s", content)  # Log the original content

    cleaned_content = re.sub('<[^<]+?>', '', content)  # Remove HTML tags
    logging.debug("After removing HTML tags: %s", cleaned_content)

    cleaned_content = unescape(cleaned_content)  # Decode HTML entities
    logging.debug("After decoding HTML entities: %s", cleaned_content)

    # Updated regex to remove usernames based on domain patterns
    domain_regex = r'@\w+\.([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?'
    cleaned_content = re.sub(domain_regex, '', cleaned_content)  # Remove usernames based on domain
    logging.debug("After removing usernames: %s", cleaned_content)

    cleaned_content = re.sub(r'[^\w\s.,!?;:]', '', cleaned_content)  # Remove special characters
    logging.debug("After removing special characters: %s", cleaned_content)

    cleaned_content = re.sub(r':\w+:', '', cleaned_content)  # Remove words enclosed with colons
    logging.debug("After removing words enclosed with colons: %s", cleaned_content)

    return cleaned_content