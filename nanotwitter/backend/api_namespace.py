import http.client
from datetime import datetime
from flask_restplus import Namespace, Resource, fields
from nanotwitter.backend import config
from nanotwitter.backend.models import TweetModel
from nanotwitter.backend.token_validation import validate_token_header
from nanotwitter.backend.db import db
from flask import abort

api_namespace = Namespace('api', description='API operations')


def authentication_header_parser(value):
    username = validate_token_header(value, config.PUBLIC_KEY)
    if username is None:
        abort(401)
    return username


# Input and output formats for tweet

authentication_parser = api_namespace.parser()
authentication_parser.add_argument('Authorization', location='headers',
                                   type=str,
                                   help='Bearer Access Token')

tweet_parser = authentication_parser.copy()
tweet_parser.add_argument('text', type=str, required=True,
                            help='Text of the tweet')

model = {
    'id': fields.Integer(),
    'username': fields.String(),
    'text': fields.String(),
    'timestamp': fields.DateTime(),
}
tweet_model = api_namespace.model('tweet', model)


@api_namespace.route('/me/tweets/')
class MeTweetListCreate(Resource):

    @api_namespace.doc('list_tweets')
    @api_namespace.expect(authentication_parser)
    @api_namespace.marshal_with(tweet_model, as_list=True)
    def get(self):
        """
        Returns all tweets
        """
        args = authentication_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])

        tweets = (TweetModel
                    .query
                    .filter(TweetModel.username == username)
                    .order_by('id')
                    .all())
        return tweets

    @api_namespace.doc('create_tweet')
    @api_namespace.expect(tweet_parser)
    @api_namespace.marshal_with(tweet_model, code=http.client.CREATED)
    def post(self):
        """
        Create a new tweet
        """
        args = tweet_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])

        new_tweet = TweetModel(username=username,
                                   text=args['text'],
                                   timestamp=datetime.utcnow())
        db.session.add(new_tweet)
        db.session.commit()

        result = api_namespace.marshal(new_tweet, tweet_model)

        return result, http.client.CREATED


search_parser = api_namespace.parser()
search_parser.add_argument('search', type=str, required=False,
                            help='Search in the text of the tweets')


@api_namespace.route('/tweets/')
class TweetList(Resource):

    @api_namespace.doc('list_tweets')
    @api_namespace.marshal_with(tweet_model, as_list=True)
    @api_namespace.expect(search_parser)
    def get(self):
        """
        Retrieves all the tweets
        """
        args = search_parser.parse_args()
        search_param = args['search']
        query = TweetModel.query
        if search_param:
            query = (query.filter(TweetModel.text.contains(search_param)))

        query = query.order_by('id')
        tweets = query.all()

        return tweets


@api_namespace.route('/tweets/<int:tweet_id>/')
class TweetsRetrieve(Resource):

    @api_namespace.doc('retrieve_tweet')
    @api_namespace.marshal_with(tweet_model)
    def get(self, tweet_id):
        """
        Retrieve a tweet
        """
        tweet = TweetModel.query.get(tweet_id)
        if not tweet:
            # The tweet is not present
            return '', http.client.NOT_FOUND

        return tweet
