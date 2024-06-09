from markovchain.text import MarkovText
from clean import clean_content

def retrieve_posts(client, client_did):
    post_list = []
    has_more = True
    cursor = None  # Initialize cursor for pagination

    while has_more:
        try:
            if cursor:
                posts = client.app.bsky.feed.post.list(client_did, limit=100, cursor=cursor)
            else:
                posts = client.app.bsky.feed.post.list(client_did, limit=100)
        except Exception as e:
            print(f"Error fetching posts: {e}")
            break

        if not posts.records.items():
            print("No more posts found.")
            break

        for post in posts.records.items():
            post_list.append(post)

        # Check if the response has a cursor for pagination
        cursor = getattr(posts, 'next_cursor', None)
        has_more = bool(cursor)  # Continue if there is a next_cursor

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
    
    # Debugging: Print structure of the first post
    if posts:
        print("First post structure:", posts[0])
    
    # Adjusted list comprehension to handle tuples and access text field from Record instance
    return [clean_content(post[1].text) for post in posts if hasattr(post[1], 'text')]
