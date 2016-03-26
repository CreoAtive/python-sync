# python
import sys
import os

# modules
import sync
import utils
import repository
from config import config

fake_local = '/Users/bernhardesperester/git/cg/test'

def init():
    '''init repository'''

    try:
        repository.init()

        config.save()
    except Exception as e:
        print e.message

def push(target = '', origin = '', *args):
    '''push local to remote'''

    if target == 'remote':
        url = config.getRemote(origin)

        if url:
            local = utils.getCurrentWorkingDir()
            #local = fake_local

            local += '/'

            print 'push repository to {url}'.format(url = url)

            sync_result = sync.push(local, url)

            print 'done syncing {files_count} files'.format(files_count = len(sync_result.getFiles()))

def pull():
    '''pull remote to local'''

    url = config.getRemote('origin')

    if url:
        local = utils.getCurrentWorkingDir()
        #local = fake_local

        url += '/'

        print 'pull repository from {url}'.format(url = url)

        sync_result = sync.pull(local, url)

        print 'done syncing {files_count} files'.format(files_count = len(sync_result.getFiles()))

def diff():
    '''get diff from local to remote'''
    pass

def clone(url = '', *args):
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

                pull()
            except Exception as e:
                print e.message
        except Exception as e:
            print e.message

def setRemote(origin = '', url = '', *args):
    '''set remote url'''

    print 'set remote {origin} to {url}'.format(origin = origin, url = url)

    config.setRemote(origin, url)
    config.save()

def removeRemote(origin = '', *args):
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

def main(args = []):
    '''main method'''
    if args:
        method = args.pop(0)

        if method == 'init':
            return init()

        if method == 'clone':
            return clone(*args)

        if method == 'push':
            return push(*args)

        if method == 'pull':
            return pull()

        if method == 'set-remote':
            return setRemote(*args)

        if method == 'remove-remote':
            return removeRemote(*args)

    return showHelp()

if __name__ == '__main__':
    main(sys.argv[1:])
