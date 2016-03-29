# python
import sys
import os

# modules
import sync
import utils
import repository
from config import config

fake_local = '/Users/bernhardesperester/git/cg/test'
fake_local = 'D:/git/cg/test'

def init():
    '''init repository'''

    try:
        repository.init()

        config.save()
    except Exception as e:
        print e.message

def push(origin = '', *args, **kwargs):
    '''push local to remote'''

    url = config.getRemote(origin)

    if url:
        local = utils.getCurrentWorkingDir()
        #local = fake_local

        local += '/'

        print 'push repository to {url}'.format(url = url)

        sync_result = sync.push(local, url, *args, **kwargs)

        print 'done syncing {files_count} files'.format(files_count = len(sync_result.getFiles()))

def pull(*args, **kwargs):
    '''pull remote to local'''

    url = config.getRemote('origin')

    if url:
        local = utils.getCurrentWorkingDir()
        #local = fake_local

        url += '/'

        print 'pull repository from {url}'.format(url = url)

        sync_result = sync.pull(local, url, *args, **kwargs)

        print 'done syncing {files_count} files'.format(files_count = len(sync_result.getFiles()))

def diff():
    '''get diff from local to remote'''
    pass

def clone(url = '', *args, **kwargs):
    '''clone repository from remte url'''

    if url:
        dirname, basename = os.path.split(url)

        try:
            repository_path = os.path.join(utils.getCurrentWorkingDir(), basename)

            utils.makeDirs(repository_path)

            try:
                utils.setCurrentWorkingDir(repository_path)

                init()

                config.setRemote('origin', url)
                config.save()

                pull(*args, **kwargs)
            except Exception as e:
                print e.message
        except Exception as e:
            print e.message

def setRemote(origin = '', url = '', *args, **kwargs):
    '''set remote url'''

    print 'set remote {origin} to {url}'.format(origin = origin, url = url)

    config.setRemote(origin, url)
    config.save()

def removeRemote(origin = '', *args, **kwargs):
    '''remove origin'''
    pass

def showHelp():
    '''show help'''

    print '''Help

init                            Initialize empty repository
clone <url>                     Clone from remote repository
push <origin>                   Push to remote repository
pull                            Pull from remote repository
set-remote <origin> <url>       Set remote repository url
remove-remote <origin>          Remove repository'''

def prepArgs(*args):
    prepped_args = []
    prepped_kwargs = {}

    for arg in args:
        if '=' in arg:
            kwarg, kwarg_value = arg.split('=', 2)

            if kwarg:
                prepped_kwargs[kwarg] = kwarg_value
        else:
            prepped_args.append(arg)

    return prepped_args, prepped_kwargs

def main(args = []):
    '''main method'''
    if args:
        method = args.pop(0)

        args, kwargs = prepArgs(*args)

        if method == 'init':
            return init()

        if method == 'clone':
            return clone(*args, **kwargs)

        if method == 'push':
            return push(*args, **kwargs)

        if method == 'pull':
            return pull()

        if method == 'set-remote':
            return setRemote(*args, **kwargs)

        if method == 'remove-remote':
            return removeRemote(*args, **kwargs)

    return showHelp()

if __name__ == '__main__':
    main(sys.argv[1:])
