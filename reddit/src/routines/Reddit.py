import logging
import pandas as pd
from reddit.src.framework.Connector import Connector
from reddit.src.framework.SentimentAnalyzer import SentimentAnalyzer


class Reddit(object):
    """
    This class collects data from reddit api
    """

    def __init__(self, namespace, subreddits):
        self.__namespace = namespace
        self.__subreddits = subreddits

    def get_subreddit(self, limit) -> int:
        """
        This method executes the connection to a given api and returns the data from api
        :return: df with reddit data
        """
        all_posts = []
        df = pd.DataFrame

        bert = SentimentAnalyzer()

        try:
            namespace = self.__namespace
            api_con = Connector(username=namespace.username, password=namespace.password, client_id=namespace.client_id,
                                secret_token=namespace.secret_token, header_info=namespace.header_info,
                                grant_type=namespace.grant_type, url=namespace.url, oauth_url=namespace.oauth_url,
                                proxy=namespace.proxy)

            reddit = api_con.praw_connector()

            for subreddit in self.__subreddits:
                posts = reddit.subreddit(subreddit).hot(limit=limit)

                for post in posts:
                    all_posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments,
                                      post.selftext, post.created])

                    df = pd.DataFrame(all_posts, columns=['title', 'score', 'id', 'subreddit', 'url',
                                                          'num_comments', 'body', 'created'])

                sentiments = bert.analyze_data(df)

                new_df = pd.merge(df, sentiments, on='title')

                new_df.to_csv('output.csv')

        except Exception as e:
            logging.error(f'Something went wrong while fetching the data: {e}')

        return 0

