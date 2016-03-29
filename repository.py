# python
import os
import datetime

# modules
import utils

REPOSITORY_DIR = '.repository'
REPOSITORY_BACKUP_DIR = REPOSITORY_DIR + '/backups/{date}'.format(date = datetime.datetime.today().strftime('%Y%m%d'))

def init():
    '''init repository'''
    try:
        utils.makeDirs(getPath())
    except Exception as e:
        raise Exception('could not init repository. reason: {reason}'.format(reason = e.message))

def getPath():
    '''get repository path'''
    return os.path.join(utils.getCurrentWorkingDir(), REPOSITORY_DIR)

def exists():
    '''check if repository exists'''
    return os.path.isdir(getPath())
