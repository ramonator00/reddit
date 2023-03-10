import logging
import praw
import requests
from requests.auth import HTTPBasicAuth

class Connector(object):
    """
    This class is used to manage the authentication of ani api
    """
    def __init__(self, username: str, password: str, client_id: str, secret_token: str,
                 header_info: str, grant_type: str, url: str, oauth_url: str, proxy: str):
        self.__username = username
        self.__password = password
        self.__client_id = client_id
        self.__secret_token = secret_token
        self.__proxy = proxy
        self.__header_info = header_info
        self.__grant_type = grant_type
        self.__url = url
        self.__oauth_url = oauth_url

    def __prepare_header(self) -> dict:
        """
        This method prepares the header for executing a request
        :return: header_info as dict
        """
        return {'User-Agent': f'{self.__header_info}/0.0.1'}

    def __prepare_req_data(self) -> dict:
        """
        This method generates a dict for request data
        :return: data for request
        """
        return {'grant_type': f'{self.__grant_type}',
                'username': f'{self.__username}',
                'password': f'{self.__password}'}

    def __prepare_proxy(self) -> dict:
        """
        This method returns a proxy as dict.
        :return: proxy as dict
        """
        return {'http': f'{self.__proxy}',
                'https': f'{self.__proxy}'}

    def oauth_connect(self) -> tuple:
        """
        This method executes a connection.
        The token is valid (~2 hours) we just add headers=headers to our requests
        :return headers: header token
        """
        session = requests.Session()
        headers = self.__prepare_header()
        data = self.__prepare_req_data()
        proxy = self.__prepare_proxy()

        try:
            auth = HTTPBasicAuth(self.__client_id, self.__secret_token)
            session.proxies = proxy
            # send our request for an OAuth token
            res = session.post(self.__url, auth=auth, data=data, headers=headers)
            # convert response to JSON and pull access_token value
            TOKEN = res.json()['access_token']
            # add authorization to our headers dictionary
            headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

        except Exception as e:
            logging.error(f'Something during connection went wrong: {e}')

        return session, headers

    def praw_connector(self) -> praw.Reddit:
        """
        Connection to Reddit API using PRAW
        :return: API Connection
        """
        return praw.Reddit(client_id=self.__client_id, client_secret=self.__secret_token, user_agent=self.__header_info)
