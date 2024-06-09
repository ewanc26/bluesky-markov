from html import unescape
import re

def clean_content(content):
    cleaned_content = re.sub('<[^<]+?>', '', content)  # Remove HTML tags
    cleaned_content = unescape(cleaned_content)  # Decode HTML entities
    cleaned_content = re.sub(r'@\w+', '', cleaned_content)  # Remove usernames
    cleaned_content = re.sub(r'[^\w\s.,!?;:]', '', cleaned_content)  # Remove special characters
    cleaned_content = re.sub(r':\w+:', '', cleaned_content)  # Remove words enclosed with colons
    
    return cleaned_content
