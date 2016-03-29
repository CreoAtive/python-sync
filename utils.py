# python
import os
import re

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

def urlPath(path):
    win_style_path_match = re.match(r'^(\w{1}:).*', path)

    if win_style_path_match:
        win_drive_letter = win_style_path_match.group(1)

        path = path.replace(win_drive_letter, '/cygdrive/{win_drive_letter}'.format(win_drive_letter = win_style_path_match.group(1)[:-1].lower()))

    return path.replace('\\', '/')
