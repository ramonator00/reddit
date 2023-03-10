import configparser
import logging

import pandas as pd


class FileHandler(object):
    """
    This class is used to read files in standard formats
    """
    def __init__(self, directory: str, file_name: str):
        self.__file_name = file_name
        self.__dir = directory

    def read_env_file(self) -> dict:
        """
        This method reads an env file with a key value structure
        :return: dict_sections as dict
        """
        dict_sections = dict
        parser = configparser.ConfigParser()

        try:
            parser.read(self.__dir + self.__file_name)
        except Exception as e:
            logging.error(f'something went wrong while reading the file: {e}')

        for section in parser.sections():
            dict_sections = dict(parser.items(section))

        return dict_sections

    def read_csv(self, attribute) -> list:
        """
        This method return a list of given csv file attribute
        :attribute: Desired Column Name of a given csv file
        :return: List of Dataframe Column
        """
        df = pd.read_csv(self.__dir + self.__file_name)

        df_list = df[attribute].to_list()

        return df_list


