from nanotwitter_pg.backend.config import PRIVATE_KEY
from nanotwitter_pg.backend.token_validation import generate_token_header as token_generator

if __name__ == '__main__':
    token = token_generator('admin', PRIVATE_KEY)
    print(token)