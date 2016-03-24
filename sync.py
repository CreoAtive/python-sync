import sys
import subprocess
import os

source = '/cygdrive/d/git/cg/onTheHunt/assets/girl/cg-exchange/output-mari'
target = 'ssh-w0082e65@git.esperester.com:/www/htdocs/w0082e65/git.esperester.com/cg/onTheHunt/assets/girl/cg-exchange/output-mari'

def diff(source, target):
    diff_cmd = ['rsync', '-avnc', '-e ssh', source, target]

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

for arg in sys.argv[1:]:
    if arg == 'diff':
        paths = diff(source, target)

        print '{files} have been changed'.format(files = len(paths))

        if '-v' in sys.argv[2:]:
            for path in paths:
                print path['name']
        #print [path['name'] for path in paths]
