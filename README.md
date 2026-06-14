# Bluesky Markov Bot

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

This repository contains a set of scripts to create and post Markov chain-generated content to a Bluesky account using data retrieved from another Bluesky account.

> 🧶 Also available on [Tangled](https://tangled.org/ewancroft.uk/bluesky-markov)

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Logging](#logging)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Fetches posts from a specified source account.
- Cleans and processes the retrieved content to ensure quality.
- Utilises Markov chain text generation to create new posts.
- Automatically posts generated content to a designated destination account.
- Logs all significant events and errors for debugging purposes.

## Requirements

To run this project, you will need the following:

- Rust 1.85+ (Cargo)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ewanc26/bluesky-markov.git
   cd bluesky-markov
   ```

2. Build the project:

   ```bash
   cargo build --release
   ```

3. Create a `.env` file in the root directory of the project and add your environment variables:

   ```plaintext
   SOURCE_HANDLE=your_source_handle
   DESTINATION_HANDLE=your_destination_handle
   CHAR_LIMIT=280
   SRC_APP_PASS=your_source_app_password
   DST_APP_PASS=your_destination_app_password
   BSKY_HOST_URL=https://bsky.social # Optional: defaults to bsky.social
   ```

## Usage

1. Navigate to the project directory.
2. Run the application:

   ```bash
   cargo run --release
   ```

The application will log into the source and destination accounts, retrieve posts, generate new content based on the retrieved posts, and post the generated content to the destination account at random intervals.

## Logging

All logs are stored in the `log` directory. The logs are written to `general.log`, where you can find details about the application's execution, including:

- Successful logins
- Retrieved posts
- Generated content
- Errors and exceptions

## File Structure

The project has the following structure:

```plaintext
project-root/
│
├── log/
│   └── general.log           # Log file for application events
│
├── src/
│   ├── bsky.rs               # Bluesky API interaction (using bsky-sdk)
│   ├── clean.rs              # Content cleaning logic
│   ├── markov_gen.rs         # Markov chain generation
│   ├── time.rs               # Time and scheduling utilities
│   └── main.rs               # Main application entry point
│
├── .env                       # Environment variables for authentication
├── Cargo.toml                 # Rust dependencies and configuration
└── README.md                  # Project documentation
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or find bugs, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## ☕ Support

If you found this useful, consider [buying me a ko-fi](https://ko-fi.com/ewancroft)!
