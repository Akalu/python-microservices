import http.client
from flask_restplus import Namespace, Resource
from nanotwitter.backend.models import TweetModel
from nanotwitter.backend.db import db

admin_namespace = Namespace('admin', description='Admin operations')


@admin_namespace.route('/tweets/<int:tweet_id>/')
class TweetsDelete(Resource):

    @admin_namespace.doc('delete_tweet',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, tweet_id):
        """
        Delete a tweet
        """
        tweet = TweetModel.query.get(tweet_id)
        if not tweet:
            # The tweet is not present
            return '', http.client.NO_CONTENT

        db.session.delete(tweet)
        db.session.commit()

        return '', http.client.NO_CONTENT
