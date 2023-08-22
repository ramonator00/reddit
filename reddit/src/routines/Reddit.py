import logging
from typing import Type

import pandas as pd
from pandas import DataFrame

from reddit.src.framework.Connector import Connector
from reddit.src.framework.SentimentAnalyzer import SentimentAnalyzer


class Reddit(object):
    """
    This class collects data from reddit api
    """

    def __init__(self, namespace, subreddits):
        self.__namespace = namespace
        self.__subreddits = subreddits

    def get_subreddit(self, limit: int, search_term: list) -> Type[DataFrame]:
        """
        This method executes the connection to a given api and returns the data from api
        :limit: number of subreddits
        :search_term: list of search terms
        :return: df with subreddits data
        """
        all_posts = []
        df = pd.DataFrame
        new_df = pd.DataFrame

        bert = SentimentAnalyzer()

        try:
            namespace = self.__namespace
            api_con = Connector(username=namespace.username, password=namespace.password, client_id=namespace.client_id,
                                secret_token=namespace.secret_token, header_info=namespace.header_info,
                                grant_type=namespace.grant_type, url=namespace.url, oauth_url=namespace.oauth_url,
                                proxy=namespace.proxy)

            reddit = api_con.praw_connector()

            for subreddit in self.__subreddits:
                posts = reddit.subreddit(subreddit)

                for query in search_term:

                    for post in posts.search(query):
                        all_posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments,
                                          post.selftext, post.created])

                        df = pd.DataFrame(all_posts, columns=['title', 'score', 'id', 'subreddit', 'url',
                                                              'num_comments', 'body', 'created'])

                    sentiments = bert.analyze_data(df)

                    new_df = pd.merge(df, sentiments, on='title')

                    new_df.to_csv('output_cs_buri_1.csv', sep=';')

        except Exception as e:
            logging.error(f'Something went wrong while fetching subreddits: {e}')

        return new_df

    def get_comments(self, limit: int, search_term: list) -> Type[DataFrame]:
        """
        This method reads comments from reddit
        :limit: Number of subreddits
        :search_term: list of search terms
        :return: df with comments
        """
        df_comments = pd.DataFrame
        all_comments = []

        try:
            namespace = self.__namespace
            api_con = Connector(username=namespace.username, password=namespace.password, client_id=namespace.client_id,
                                secret_token=namespace.secret_token, header_info=namespace.header_info,
                                grant_type=namespace.grant_type, url=namespace.url, oauth_url=namespace.oauth_url,
                                proxy=namespace.proxy)

            reddit = api_con.praw_connector()

            subreddits = self.get_subreddit(limit, search_term)

            for id in subreddits['id']:
                submission = reddit.submission(id=id)

                for comment in submission.comments:
                    all_comments.append([id, comment.body])
                    df_comments = pd.DataFrame(all_comments, columns=['id', 'comment'])

        except Exception as e:
            logging.error(f'Something went wrong while fetching comments from reddit: {e}')

        return df_comments

    def merge_requests(self, limit: int, search_term: list) -> DataFrame:
        """
        This method merges all requests together
        :limit: Number of subreddits
        :search_term: list of search terms
        :return: df_merged
        """
        subreddits = self.get_subreddit(limit, search_term)
        comments = self.get_comments(limit, search_term)

        merged_df = pd.merge(subreddits, comments, on='id')

        print(merged_df)

        merged_df.to_csv('withcomments.csv')

        return merged_df



