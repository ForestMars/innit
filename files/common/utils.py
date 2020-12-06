# utils.py - Commonly used helper functions to handle mundane operations safely.
__version__ = '0.2'

import csv
import hashlib
import json
import os
import subprocess # Currently used only with Hadoop.
import sys
from pathlib import Path
from contextlib import ContextDecorator, _GeneratorContextManager
from functools import wraps

# This is for an older version and can be removed.
try:
    import cPickle as pickle
except ImportError:
    import pickle


#import logger
#logger = logging.getLogger(__name__)
log = print


class HaltException(Exception): pass

class ContextManager_(_GeneratorContextManager, ContextDecorator): pass


# Decorator for writing to filesystem.
def exists(func):
    @wraps(func)
    def inner(*args, **kwds):
        filepath = args[0]
        wrb = args[1]
        path = os.path.split(filepath)[0]
        if path is None:
            return ContextManager_(func, args, kwds)
        if path_exists(path):
            if isdir(path):
                return ContextManager_(func, args, kwds)
            else: # target is not a directory.
                # raise
                log('nocando.')
        else: # directory doesn't exist; creating.
            try:
                mkdir(path)
            except Exception as e:
                log(e)
        return ContextManager_(func, args, kwds)
    return inner

@exists
def fopen(filepath, mode):
    file = open(filepath, mode)
    yield file
    file.close()


## file system utilities

def get_reg_files(dir: str, ext: str='txt') -> list:
    """ Decorator for all filesystem fetching operations. Returns list of entries for given directory, excuding hidden files. """
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.abspath(os.path.join(dir, f))) and not f.startswith('.')]
    return files

def get_dir_list(dir: str) -> list:
    return [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir,d))]

def isdir(path, dir=None):
    return os.path.isdir(path)

def path_exists(path):
    return os.path.exists(path)

def mkdir(path, dir=None):
    if dir is not None and not isdir(path, dir):
        try:
            os.mkdir(path + '/' + dir)
        except Exception as e:
            # @TODO: Only create directories if they don't already exist.
            pass
    else:
        if not os.path.isdir(path):
            try:
                Path(path).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print('error')
                # @TODO: Only create directories if they don't already exist.
                pass

def file_util(file: str, dir: str='.'):
    """ Placeholder for file utility """
    pass

def read_file(file: str, dir: str='.'):
    f = open(file, "r")
    return f.read()

def write_file(contents, file: str, dir: str='.'):
    # @TODO: parse filepath
    f = open("file", "rw")
    f.write(contents)
    f.close()

def append_file(contents, file: str, dir: str='.'):
    f = open(file, "a")
    f.write(contents)
    f.close()

# O(n) feels so dirty.
def glob_nom(glob):
    for objname, oid in globals().items():
        if oid is glob:
            return objname

def str_to_cls(s):
    if s in globals() and isinstance(globals()[s], types.ClassType):
            return globals()[s]
    return None

def move_file(*args, **kwargs):
    """ This is just a wrapper for move_posix_file() as the most common use case. """
    move_posix_file(*args, **kwargs)

def move_posix_file(file, old, new):
    """ Uproots target and sets it on a new path. """
    file = '/' + file
    os.rename(old + file, new + file)

def rename_file(path, old, new):
    """ @TODO: merge with move_file """
    os.rename(path + old, path + new)

def move_hdfs_file(file, old, new):
    """ Move a file within a Hadoop cluster """
    # kwargs = (shell=True, stdout=PIPE, stderr=PIPE)
    find = os.popen('hadoop fs -ls -R ' + file).read().split(' ')
    if len(find) > 0:
        move_it = subprocess.run(find[6], kwargs)
        move = 'hdfs dfs -mv file new'
        move_it = subprocess.run(move, kwargs)

        if mfind_it.returncode == 0 and move_it.returncode == 0:
            log("Successfully moved %s" % file)
        else:
            log("Failed to update hdfs target.")

def move_topic(node, new_topic):
    pass

def update_parent(node, old, new):
    """ Change parentage of a given node or object. """
    pass

def merge_lists(list1, list2):
    """ Does what it says on the tin. """
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list

def dump_pill():
    """ Retrieve all pill metadata. """
    pass

def md5_hash(obj, len=4):
    m = hashlib.md5()
    m.update(json.dumps(obj).encode('utf-8'))
    return (m.hexdigest()[:len])

def redirect_sysout_to_file(obj, filename: str):
    """ Mainly for printing to a file
    :param obj: a printable thing
    :param filename: a file to print it to """
    orig_stdout = sys.stdout
    with open(filename, 'w') as file:
        sys.stdout = file
        print(obj)
    sys.stdout = orig_stdout
