# python
import os
import re
import subprocess

# modules
import utils

rsync_options = {
    'checksum': '-c',
    'recursive': '-r',
    'verbose': '-v',
    'update': '-u',
    'links': '-l',
    'perms': '-p',
    'owner': '-o',
    'group': '-g',
    'times': '-t',
    'dry': '-n',
    'compress': '-z',
    'delete': '--delete',
    'ignore_times': '--ignore-times',
    'size_only': '--size-only',
    'progress': '--progress',
    'itemize_changes': '--itemize-changes'
}

class SyncResult:
    '''an object containing all information about the sync'''

    def __init__(self, files = []):
        self._files = files

    def getFiles(self):
        return self._files

def compileOptions(options):
    args = []
    kwargs = []
    options_compiled = []

    for option_name in options:
        if option_name in rsync_options:
            option = rsync_options[option_name]

            if option.startswith('--'):
                kwargs.append(option)
            else:
                args.append(option[1:])

    if args:
        options_compiled =  ['-{args}'.format(args = ''.join(args))]

    if kwargs:
        options_compiled += kwargs

    return options_compiled

def push(local = '', remote = '', dry = False):
    '''push from local to remote'''
    if local and remote:
        options = ['checksum', 'recursive', 'verbose', 'links', 'perms', 'owner', 'group', 'times', 'compress', 'progress', 'delete']

        if dry:
            options.append('dry')

        options_compiled = compileOptions(options)

        push_cmd = filter(bool, ['rsync', '-e ssh'] + options_compiled + ['--exclude=.repository', local, remote])

        print push_cmd

        popen = subprocess.Popen(push_cmd, stdout = subprocess.PIPE)

        #print popen.stdout.read()

        files = []

        try:
            for line in iter(popen.stdout.readline, b''):
                stripped_line = line.strip()

                print stripped_line

                root, extension = os.path.splitext(stripped_line)

                if re.match(r'[\w\d]+', extension[1:]) and not utils.isDigit(extension[1:]):
                    files.append(stripped_line)
        except Exception as e:
            print e.message
        finally:
            return SyncResult(files)

def pull(local = '', remote = '', dry = False):
    '''pull from remote to local'''

    return push(remote, local, dry)

def diff():
    '''get diff from local to remote'''
    pass
