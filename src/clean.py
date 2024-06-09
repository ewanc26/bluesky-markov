from html import unescape
import re

# Function to clean HTML content and special characters from posts
def clean_content(content):
    # Remove HTML tags
    cleaned_content = re.sub('<[^<]+?>', '', content)
    # Decode HTML entities
    cleaned_content = unescape(cleaned_content)
    # Remove usernames
    cleaned_content = re.sub(r'@\w+', '', cleaned_content)
    # Remove special characters except standard punctuation
    cleaned_content = re.sub(r'[^\w\s.,!?;:]', '', cleaned_content)
    # Remove words enclosed with colons
    cleaned_content = re.sub(r':\w+:', '', cleaned_content)
    
    return cleaned_content
