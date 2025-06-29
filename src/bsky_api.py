from atproto import IdResolver, Client
import os
import logging

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

def login(handle_env_var, app_pass_env_var):
    try:
        handle = os.getenv(handle_env_var)
        app_pass = os.getenv(app_pass_env_var)
        host_url = os.getenv("BSKY_HOST_URL", "https://bsky.social")

        client = Client(host_url)

        if not handle or not app_pass:
            logging.error("Handle or app password missing in environment variables.")
            raise ValueError("Handle or app password missing in environment variables")

        logging.debug("Attempting to log in with handle: %s", handle)
        client.login(handle, app_pass)  # Access credentials securely

        logging.info("Login successful for handle: %s", handle)
        return client
    
    except Exception as e:
        logging.exception("An error occurred during login: %s", e)
        quit(1)

def DID_resolve(handle):
    try:
        logging.debug("Resolving DID for handle: %s", handle)
        resolver = IdResolver()
        did = resolver.handle.resolve(handle)
        logging.debug("Resolved DID: %s", did)

        did_doc = resolver.did.resolve(did)
        logging.debug("Resolved DID Document: %s", did_doc)

        package = {"did": did, "did_doc": did_doc}
        logging.info("Successfully resolved DID and DID Document.")

        return package

    except Exception as e:
        logging.exception("An error occurred while resolving DID: %s", e)
        return None