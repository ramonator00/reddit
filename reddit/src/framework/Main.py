from reddit.src.framework.Controller import Controller
from reddit.src.framework.FileHandler import FileHandler
from reddit.src.routines.Reddit import Reddit

if __name__ == '__main__':

    # FIXME: This main is horrible and has to be organized at the end

    #directory = input('Please enter your src directory: ')

    f = FileHandler('C:/Users/ramon/Workspace/reddit/reddit/src', '/.env')
    fh_subred = FileHandler('C:/Users/ramon/Workspace/reddit/reddit/src/data', '/subreddits.csv')

    e = f.read_env_file()
    x = Controller(e)
    namespace = x.read_config()
    subreddits = fh_subred.read_csv('subreddits')

    search_terms = ['pibslers']

    r = Reddit(namespace, subreddits)

    r.merge_requests(10, search_terms)
