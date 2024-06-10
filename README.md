# Bluesky Markov Bot

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

This repository contains a set of scripts to create and post Markov chain-generated content to a Bluesky account using data retrieved from another Bluesky account.

## Files

### `bsky_api.py`

Provides functions to log in to a Bluesky account and resolve DID (Decentralized Identifier).

- **Functions:**
  - `login(handle_env_var, app_pass_env_var)`: Logs in to a Bluesky account using environment variables for handle and app password.
  - `DID_resolve(handle)`: Resolves and retrieves the DID document for a given handle.

### `clean.py`

Contains a function to clean HTML content from posts.

- **Functions:**
  - `clean_content(content)`: Removes HTML tags, HTML entities, usernames, special characters, and colon-enclosed words from content.

### `markov_gen.py`

Includes functions to retrieve posts, generate Markov chain text, and refresh the Markov dataset.

- **Functions:**
  - `retrieve_posts(client, client_did)`: Retrieves posts from a Bluesky account.
  - `generate(markov, char_limit)`: Generates text using the Markov model within a character limit.
  - `refresh_dataset(markov, source_posts)`: Refreshes the Markov dataset with new posts.
  - `get_account_posts(client, client_did)`: Gets and cleans posts from a Bluesky account.

### `time_utils.py`

Provides utility functions for time calculations and sleep management.

- **Functions:**
  - `calculate_refresh_interval()`: Calculates a random refresh interval between 30 minutes to 3 hours.
  - `calculate_next_refresh(current_time, refresh_interval)`: Calculates the next refresh time.
  - `format_time_remaining(time_remaining)`: Formats the time remaining until the next refresh.
  - `sleep_until_next_refresh(next_refresh)`: Sleeps until the next refresh time.

### `main.py`

The main script to run the bot. It sets up environment variables, logs in to accounts, retrieves and processes posts, and generates and posts new content.

- **Workflow:**
  1. Load environment variables.
  2. Log in to source and destination Bluesky accounts.
  3. Retrieve and clean posts from the source account.
  4. Generate new content using the Markov model.
  5. Post generated content to the destination account.
  6. Repeat the process at calculated intervals.

### `requirements.txt`

Lists the Python dependencies required to run the scripts.

- **Dependencies:**
  - `atproto`
  - `dotenv`
  - `markovchain`

### `example.env.txt`

Example environment variables file. Copy this to `.env` and fill in your credentials.

- **Environment Variables:**
  - `SOURCE_HANDLE`: The handle of the source Bluesky account.
  - `SRC_APP_PASS`: The app password for the source Bluesky account.
  - `DST_APP_PASS`: The app password for the destination Bluesky account.
  - `DESTINATION_HANDLE`: The handle of the destination Bluesky account.
  - `CHAR_LIMIT`: The character limit for generated posts.

## Setup and Usage

1. **Clone the repository:**

   ```sh
   git clone https://github.com/ewanc26/bluesky-markov.git
   cd bluesky-markov
   ```

2. **Install the dependencies:**

   ```sh
   pip3 install -r requirements.txt
   ```

3. **Set up environment variables:**

   - Copy `example.env.txt` to `.env`:

     ```sh
     cp example.env.txt .env
     ```

   - Edit `.env` and fill in your Bluesky handles and app passwords.

4. **Run the bot:**

   ```sh
   python3 -u 'src/main.py'
   ```

## Notes

- Ensure that you have valid Bluesky handles and app passwords set in the `.env` file.
- The bot continuously runs and generates new posts at intervals between 30 minutes and 3 hours.
- Press `Ctrl+C` to stop the bot.

## Project Structure

```plaintext
bluesky-markov/
│
├── src/
│   ├── .env                    # Environment configuration file
│   ├── bsky_api.py             # Module for Bluesky API interactions
│   ├── clean.py                # Module for cleaning content
│   ├── markov_gen.py           # Module for Markov chain text generation
│   ├── main.py                 # Main script for the bot
│   ├── time_utils.py           # Module for time-related utilities
│   ├── example.env.txt         # Example environment configuration file
│
├── requirements.txt            # Python dependencies
├── LICENSE                     # Licensing file
└── README.md                   # Project README file
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
