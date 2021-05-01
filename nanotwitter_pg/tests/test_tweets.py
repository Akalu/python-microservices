"""
Test the tweets operations

Use the tweet_fixture to have data to retrieve, it generates three tweets
"""
from unittest.mock import ANY
import http.client
from freezegun import freeze_time
from .constants import PRIVATE_KEY
from nanotwitter_pg.backend import token_validation
from faker import Faker
fake = Faker()


@freeze_time('2019-05-07 13:47:34')
def test_create_me_tweet(client):
    new_tweet = {
        'username': fake.name(),
        'text': fake.text(240),
    }
    header = token_validation.generate_token_header(fake.name(),
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/tweets/', data=new_tweet,
                           headers=headers)
    result = response.json

    assert http.client.CREATED == response.status_code

    expected = {
        'id': ANY,
        'username': ANY,
        'text': new_tweet['text'],
        'timestamp': '2019-05-07T13:47:34',
    }
    assert result == expected


def test_create_me_unauthorized(client):
    new_tweet = {
        'username': fake.name(),
        'text': fake.text(240),
    }
    response = client.post('/api/me/tweets/', data=new_tweet)
    assert http.client.UNAUTHORIZED == response.status_code


def test_list_me_tweets(client, tweet_fixture):
    username = fake.name()
    text = fake.text(240)

    # Create a new tweet
    new_tweet = {
        'text': text,
    }
    header = token_validation.generate_token_header(username,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/tweets/', data=new_tweet,
                           headers=headers)
    result = response.json

    assert http.client.CREATED == response.status_code

    # Get the tweets of the user
    response = client.get('/api/me/tweets/', headers=headers)
    results = response.json

    assert http.client.OK == response.status_code
    assert len(results) == 1
    result = results[0]
    expected_result = {
        'id': ANY,
        'username': username,
        'text': text,
        'timestamp': ANY,
    }
    assert result == expected_result


def test_list_me_unauthorized(client):
    response = client.get('/api/me/tweets/')
    assert http.client.UNAUTHORIZED == response.status_code


def test_list_tweets(client, tweet_fixture):
    response = client.get('/api/tweets/')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the ids are increasing
    previous_id = -1
    for tweet in result:
        expected = {
            'text': ANY,
            'username': ANY,
            'id': ANY,
            'timestamp': ANY,
        }
        assert expected == tweet
        assert tweet['id'] > previous_id
        previous_id = tweet['id']


def test_list_tweets_search(client, tweet_fixture):
    username = fake.name()
    new_tweet = {
        'username': username,
        'text': 'Do you dream about the City at the End of Time?'
    }
    header = token_validation.generate_token_header(username,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/tweets/', data=new_tweet,
                           headers=headers)
    assert http.client.CREATED == response.status_code

    response = client.get('/api/tweets/?search=City')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the returned values contain "city"
    for tweet in result:
        expected = {
            'text': ANY,
            'username': username,
            'id': ANY,
            'timestamp': ANY,
        }
        assert expected == tweet
        assert 'city' in tweet['text'].lower()


def test_get_tweet(client, tweet_fixture):
    tweet_id = tweet_fixture[0]
    response = client.get(f'/api/tweets/{tweet_id}/')
    result = response.json

    assert http.client.OK == response.status_code
    assert 'text' in result
    assert 'username' in result
    assert 'timestamp' in result
    assert 'id' in result


def test_get_non_existing_tweet(client, tweet_fixture):
    tweet_id = 123456
    response = client.get(f'/api/tweets/{tweet_id}/')

    assert http.client.NOT_FOUND == response.status_code
