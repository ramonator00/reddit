from types import SimpleNamespace

from reddit.src.framework.FileHandler import FileHandler


class Controller(object):
    """
    This class controls the dependencies between the classes
    """
    def __init__(self, config_dict: dict):
        self.__dict = config_dict

    def read_config(self):
        """
        This method reads the config dict and writes it into a variable
        :return:
        """
        return SimpleNamespace(**self.__dict)
