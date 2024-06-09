from atproto import IdResolver, Client
import os
import dotenv

def login(handle_env_var, app_pass_env_var):
    try:
        dotenv.load_dotenv()
        handle = os.getenv(handle_env_var)
        app_pass = os.getenv(app_pass_env_var)

        if not handle or not app_pass:
            raise ValueError("Handle or app password missing in environment variables")

        client = Client()
        client.login(handle, app_pass)  # Access credentials securely

        return client
    
    except Exception as e:
        print(e)
        quit(1)

def DID_resolve(handle):
    try:
        resolver = IdResolver()
        did = resolver.handle.resolve(handle)
        did_doc = resolver.did.resolve(did)

        package = {"did": did, "did_doc": did_doc}

        return package
    except Exception as e:
        print(e)
        return None
