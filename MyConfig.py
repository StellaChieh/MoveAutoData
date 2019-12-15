import ConfigParser
import os
import sys

receiver_file = 'config/receivers.txt'
db_config = 'config/odbc.properties'
token_original_folder = 'Token'
token_fail_folder = 'TokenFail'
token_done_folder = 'TokenDone'
log_folder = 'Log'


def get_absolute_path(file):
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    return os.path.join(dirname, file)


def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def get_receivers():
    with open(get_absolute_path(receiver_file), 'r') as f:
        return [line.rstrip() for line in f]


def get_db_config():
    config = ConfigParser.RawConfigParser()
    config.read(get_absolute_path(db_config))
    db_dict = {'ip': config.get('DbConfig', 'ip'),
               'database': config.get('DbConfig', 'database'),
               'user': config.get('DbConfig', 'user'),
               'password': config.get('DbConfig', 'password')}
    return db_dict


def get_token_ori_folder():
    folder = get_absolute_path(token_original_folder)
    make_dir(folder)
    return folder


def get_token_fail_folder():
    folder = get_absolute_path(token_fail_folder)
    make_dir(folder)
    return folder


def get_token_done_folder():
    folder = get_absolute_path(token_done_folder)
    make_dir(folder)
    return folder


def get_log_folder():
    folder = get_absolute_path(log_folder)
    make_dir(folder)
    return folder


if __name__ == '__main__':
    r = get_receivers()
    print r
    d = get_db_config()
    print d
