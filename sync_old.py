import sys
import subprocess
import os
import json
import datetime

source = '/cygdrive/d/git/cg/onTheHunt/assets/girl/cg-exchange/output-mari'
origin = 'ssh-w0082e65@git.esperester.com:/www/htdocs/w0082e65/git.esperester.com/cg/onTheHunt/assets/girl/cg-exchange/output-mari'

def diff(source, origin):
    diff_cmd = ['rsync', '-avnc', '-e ssh', source, origin]

    popen = subprocess.Popen(diff_cmd, stdout = subprocess.PIPE)

    source_basename = os.path.basename(source)

    paths = []

    for line in iter(popen.stdout.readline, b''):
        if line.startswith(source_basename):
            path = line.strip()

            diff_dirname, diff_basename = os.path.split(path)

            if diff_basename:
                paths.append({
                    'path': diff_dirname,
                    'name': diff_basename
                })

    return paths

def makedirs(path):
    if os.path.isdir(path):
        return True
    else:
        try:
            os.makedirs(path)
        except Exception as e:
            print e.message

            return False
        else:
            return True

    return False

def init():
    sync_dir.init()

    logger.init()

    config.init()

    if sync_dir.exists() and logger.exists() and config.exists():
        print 'Repository has been initialized'

class SyncDir:

    def __init__(self):
        self._path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.sync')

    def init(self):
        makedirs(self._path)

        return self

    def exists(self):
        return os.path.isdir(self._path)

    def getPath(self):
        return self._path

class Logger:

    def __init__(self, sync_dir = None):
        self._sync_dir = sync_dir

    def init(self):
        if not self.exists():
            if self._sync_dir and self._sync_dir.exists():
                self.log('Created Logfile')

    def getPath(self):
        if self._sync_dir and self._sync_dir.exists():
            return os.path.join(self._sync_dir.getPath(), 'log.md')

        return ''

    def exists(self):
        if self.getPath() and os.path.isfile(self.getPath()):
            return True

        return False

    def log(self, message = None):
        assert isinstance(message, basestring), 'log: message must be an instance of basestring'

        with open(self.getPath(), 'a') as outfile:
            outfile.write('{datetime}: {message}\n'.format(datetime = datetime.datetime.now(), message = message))

class Config:

    def __init__(self, sync_dir = None, logger = None):
        self._sync_dir = sync_dir
        self._logger = logger
        self._origin = None
        self._remotes = {
            'origin': None
        }
        self._changes = []



        self._default_config = {
            'remotes': self._remotes
        }

        self.load()

    def init(self):
        self.save()

    def getPath(self):
        if self._sync_dir and self._sync_dir.exists():
            return os.path.join(self._sync_dir.getPath(), 'config.json')

        return ''

    def exists(self):
        if self.getPath() and os.path.isfile(self.getPath()):
            return True

        return False

    def load(self):
        if self.exists():
            with open(self.getPath()) as json_data:
                data = json.load(json_data)

                if 'remotes' in data and data['remotes']:
                    self.setRemotes(data['remotes'])

    def save(self):
        if self._sync_dir and self._sync_dir.exists():
            with open(self.getPath(), 'w') as outfile:
                json.dump(self.toDict(), outfile, sort_keys = True, indent = 2)

            if self._logger and self._logger.exists():
                for change in self.getChanges():
                    self._logger.log(change)

                self._logger.log('Saved config')

    def setRemote(self, name = None, url = None):
        assert isinstance(name, basestring), 'setRemote: name must be an instance of basestring'
        assert isinstance(url, basestring), 'setRemote: url must be an instance of basestring'

        self._remotes[name] = url

        self._changes.append('Set remote {name} to {url}'.format(name = name, url = url))

        return self

    def getRemote(self, origin = None):
        if origin in self.getRemotes():
            return self.getRemotes()[origin]

        return None

    def setRemotes(self, remotes = {}):
        assert isinstance(remotes, dict), 'setRemotes: remotes must be an instance of dict'

        self._remotes = remotes

        return self

    def getRemotes(self):
        return self._remotes

    def getChanges(self):
        return self._changes

    def toDict(self):
        return {
            'remotes': self.getRemotes()
        }

def main():
    sync_dir = SyncDir()
    logger = Logger(sync_dir = sync_dir)
    config = Config(sync_dir = sync_dir, logger = logger)

    for arg in sys.argv[1:]:
        if arg == 'diff':
            paths = diff(source, config.getRemote('origin'))

            print '{files} have been changed'.format(files = len(paths))

            if '-v' in sys.argv[2:]:
                for path in paths:
                    print path['name']
            #print [path['name'] for path in paths]

        if arg == 'init':
            init()

        if arg == 'remote':
            if sys.argv[2] == 'set-url':
                if sys.argv[3]:
                    remote_name = sys.argv[3]

                    if sys.argv[4]:
                        remote_url = sys.argv[4]

                        config.setRemote(remote_name, remote_url)
                        config.save()

                        print 'Repository remote {remote} has been updated'.format(remote = remote_name)

if __name__ == '__main__':
    main()
