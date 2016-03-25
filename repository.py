# python
import os

# modules
import utils

def init():
    '''init repository'''
    try:
        utils.makeDirs(getPath())
    except Exception as e:
        raise Exception('could not init repository. reason: {reason}'.format(reason = e.message))

def getPath():
    '''get repository path'''
    return os.path.join(utils.getCurrentWorkingDir(), '.repository')

def exists():
    '''check if repository exists'''
    return os.path.isdir(getPath())
