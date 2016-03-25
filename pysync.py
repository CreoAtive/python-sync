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

def setUrl(origin = '', url = ''):
    '''set remote url'''
    pass

def main(args = []):
    '''main method'''
    if args:
        method = args.pop(0)

        if method == 'init':
            init()

        if method == 'clone':
            clone(*args)

        if method == 'push':
            push(*args)

        if method == 'pull':
            pull()

if __name__ == '__main__':
    main(sys.argv[1:])
