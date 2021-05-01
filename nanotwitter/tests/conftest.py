import pytest
import http.client
from nanotwitter.backend.app import create_app
from .constants import PRIVATE_KEY
from nanotwitter.backend import token_validation
from faker import Faker
fake = Faker()


@pytest.fixture
def app():
    application = create_app()

    application.app_context().push()

    # Initialise the DB
    application.db.create_all()

    return application


@pytest.fixture
def tweet_fixture(client):
    '''
    Generate three tweets in the system.
    '''

    tweet_ids = []
    for _ in range(3):
        tweet = {
            'text': fake.text(240),
        }
        header = token_validation.generate_token_header(fake.name(),
                                                        PRIVATE_KEY)
        headers = {
            'Authorization': header,
        }
        response = client.post('/api/me/tweets/', data=tweet,
                               headers=headers)
        assert http.client.CREATED == response.status_code
        result = response.json
        tweet_ids.append(result['id'])

    yield tweet_ids

    # Clean up all tweets
    response = client.get('/api/tweets/')
    tweets = response.json
    for tweet in tweets:
        tweet_id = tweet['id']
        url = f'/admin/tweets/{tweet_id}/'
        response = client.delete(url)
        assert http.client.NO_CONTENT == response.status_code
