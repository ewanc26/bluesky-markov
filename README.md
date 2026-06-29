# Bluesky Markov Bot

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

Generates Markov chain posts from a Bluesky account and posts them to another.

> Also available on [Tangled](https://tangled.org/ewancroft.uk/bluesky-markov)

## Requirements

- Rust 1.85+

## Install

```bash
git clone https://github.com/ewanc26/bluesky-markov.git
cd bluesky-markov
cargo build --release
```

Create a `.env` in the project root:

```plaintext
SOURCE_HANDLE=your_source_handle
DESTINATION_HANDLE=your_destination_handle
CHAR_LIMIT=280
SRC_APP_PASS=your_source_app_password
DST_APP_PASS=your_destination_app_password
BSKY_HOST_URL=https://bsky.social
```

## Usage

```bash
cargo run --release
```

Logs into both accounts, fetches posts from the source, generates new content with Markov chains, posts to the destination at random intervals.

## Logs

Written to `log/general.log` — login status, posts fetched, content generated, errors.

## Project structure

```
├── log/general.log        # Logs
├── src/
│   ├── bsky.rs            # Bluesky API
│   ├── clean.rs           # Content cleaning
│   ├── markov_gen.rs      # Markov generation
│   ├── time.rs            # Scheduling utilities
│   └── main.rs            # Entry point
├── .env                   # Auth
└── Cargo.toml
```

## Licence

MIT
