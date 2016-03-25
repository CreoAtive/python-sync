# python
import os
import json

# modules
import utils
import repository

class Config:

    def __init__(self):
        '''init config'''
        self._remotes = {
            'origin': ''
        }

        self.load()

    def save(self):
        if repository.exists():
            try:
                with open(self.getPath(), 'w') as outfile:
                    json.dump(self.toDict(), outfile, sort_keys = True, indent = 2)
            except Exception as e:
                raise Exception('could not save config. reason: {reason}'.format(reason = e.message))

    def load(self):
        if self.exists():
            try:
                with open(self.getPath()) as json_data:
                    data = json.load(json_data)

                    if 'remotes' in data and data['remotes']:
                        self.setRemotes(data['remotes'])
            except Exception as e:
                raise Exception('could not load config. reason: {reason}'.format(reason = e.message))

    def exists(self):
        return os.path.isfile(self.getPath())

    def getPath(self):
        return os.path.join(repository.getPath(), 'config.json')

    def setRemotes(self, remotes = {}):
        '''set remote repositories'''

        assert isinstance(remotes, dict), 'setRemotes: remotes must be an instance of dict'

        self._remotes = remotes

        return self

    def getRemotes(self):
        '''get remote origins'''

        return self._remotes

    def setRemote(self, remote = '', url = ''):
        '''set remote'''

        assert isinstance(remote, basestring), 'setRemote: remote must be an instance of basestring'
        assert isinstance(url, basestring), 'setRemote: url must be an instance of basestring'

        self._remotes[remote] = url

        return self

    def getRemote(self, remote = ''):
        '''get remote by name'''
        if remote in self.getRemotes():
            return self.getRemotes()[remote]

        return ''

    def toDict(self):
        return {
            'remotes': self.getRemotes()
        }

config = Config()
