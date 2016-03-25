# python
import os

def getCurrentWorkingDir():
    return os.getcwd()

def setCurrentWorkingDir(path = ''):
    if os.path.isdir(path):
        return os.chdir(path)

    return False

def makeDirs(path = ''):
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except Exception as e:
            raise Exception('could not make dirs for path "{path}"'.format(path = path))

    return True

def isDigit(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
