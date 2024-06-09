from markovchain.text import MarkovText

def retrieve_posts(client, client_did):
    post_list = []
    has_more = True
    page = 0

    while has_more:
        try:
            posts = client.app.bsky.feed.post.list(client_did, limit=100, page=page)
        except Exception as e:
            print(f"Error fetching posts: {e}")
            break

        if not posts.records.items():
            print("No more posts found.")
            break

        for post in posts.records.items():
            post_list.append(post)

        # Update page for the next iteration
        page += 1

        # Check if there are more pages
        has_more = posts.pagination.has_more

    return post_list

def generate(markov, char_limit):
    generated_text = markov()

    if len(generated_text) > char_limit:
        generated_text = generated_text[:char_limit]

    print("Generated Text:", generated_text)

    words = generated_text.split()

    return words

def refresh_dataset(markov, source_posts):
    markov = MarkovText()

    if source_posts:
        print(f"Fetched {len(source_posts)} original posts and replies from the source account.")

    for post in source_posts:
        markov.data(post, part=True)

    markov.data('', part=False)

    return markov

def get_account_posts(client, client_did):
    posts = retrieve_posts(client, client_did)
    return [clean_content(post['content']) for post in posts]
