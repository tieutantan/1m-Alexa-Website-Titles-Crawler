import os
import ntpath
import shutil

# param <path> could either be relative or absolute.
# https://stackoverflow.com/a/41789397
def remove(path):
    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)  # remove the file
        elif os.path.isdir(path):
            shutil.rmtree(path)  # remove dir and all contains
        else:
            raise ValueError("file {} is not a file or dir.".format(path))
    except Exception:
        pass

def relative(path):
    string = root() + os.sep + path
    return string.replace(os.sep, os.path.sep)

def root():
    return os.path.dirname(os.path.abspath('run.py'))