# python
import io
import os
import re
import subprocess

# modules
import utils
import repository
import latest

INCLUDE_FILE = '.include'
EXCLUDE_FILE = '.exclude'
LATEST_FILE = '.latest'

rsync_options = {
    '--verbose': 'increase verbosity',
    '--quiet': 'suppress non-error messages',
    '--no-motd': 'suppress daemon-mode MOTD (see caveat)',
    '--checksum': 'skip based on checksum, not mod-time & size',
    '--archive': 'archive mode; equals -rlptgoD (no -H,-A,-X)',
    '--no-': 'turn off an implied OPTION (e.g. --no-D)',
    '--recursive': 'recurse into directories',
    '--relative ': 'use relative path names',
    '--backup': 'make backups (see --suffix & --backup-dir)',
    '--backup-dir': 'make backups into hierarchy based in DIR',
    '--suffix': 'backup suffix (default ~ w/o --backup-dir)',
    '--update': 'skip files that are newer on the receiver',
    '--inplace': 'update destination files in-place',
    '--append': 'append data onto shorter files',
    '--append-verify': '"--append": w/old data in file checksum',
    '--dirs': 'transfer directories without recursing',
    '--links': 'copy symlinks as symlinks',
    '--copy-links': 'transform symlink into referent file/dir',
    '--copy-unsafe-links': 'only "unsafe" symlinks are transformed',
    '--safe-links': 'ignore symlinks that point outside the tree',
    '--copy-dirlinks': 'transform symlink to dir into referent dir',
    '--keep-dirlinks': 'treat symlinked dir on receiver as dir',
    '--hard-links': 'preserve hard links',
    '--perms': 'preserve permissions',
    '--executability': 'preserve executability',
    '--chmod': 'affect file and/or directory permissions',
    '--acls': 'preserve ACLs (implies -p)',
    '--xattrs': 'preserve extended attributes',
    '--owner': 'preserve owner (super-user only)',
    '--group': 'preserve group',
    '--devices': 'preserve device files (super-user only)',
    '--specials': 'preserve special files',
    '--times': 'preserve modification times',
    '--omit-dir-times': 'omit directories from --times',
    '--super': 'receiver attempts super-user activities',
    '--fake-super': 'store/recover privileged attrs using xattrs',
    '--sparse': 'handle sparse files efficiently',
    '--dry-run': 'perform a trial run with no changes made',
    '--whole-file': 'copy files whole (w/o delta-xfer algorithm)',
    '--one-file-system': 'don\'t cross filesystem boundaries',
    '--block-size': 'force a fixed checksum block-size',
    '--rsh': 'specify the remote shell to use',
    '--rsync-path': 'specify the rsync to run on remote machine',
    '--existing': 'skip creating new files on receiver',
    '--ignore-existing': 'skip updating files that exist on receiver',
    '--remove-source-files': 'sender removes synchronized files (non-dir)',
    '--del': 'an alias for --delete-during',
    '--delete': 'delete extraneous files from dest dirs',
    '--delete-before': 'receiver deletes before transfer (default)',
    '--delete-during': 'receiver deletes during xfer, not before',
    '--delete-delay': 'find deletions during, delete after',
    '--delete-after': 'receiver deletes after transfer, not before',
    '--delete-excluded': 'also delete excluded files from dest dirs',
    '--ignore-errors': 'delete even if there are I/O errors',
    '--force': 'force deletion of dirs even if not empty',
    '--max-delete': ' don\'t delete more than NUM files',
    '--max-size': 'don\'t transfer any file larger than SIZE',
    '--min-size': 'don\'t transfer any file smaller than SIZE',
    '--partial': 'keep partially transferred files',
    '--partial-dir': 'put a partially transferred file into DIR',
    '--delay-updates': 'put all updated files into place at end',
    '--prune-empty-dirs': 'prune empty directory chains from file-list',
    '--numeric-ids': 'don\'t map uid/gid values by user/group name',
    '--timeout': 'set I/O timeout in seconds',
    '--contimeout': 'set daemon connection timeout in seconds',
    '--ignore-times': 'don\'t skip files that match size and time',
    '--size-only': 'skip files that match in size',
    '--modify-window': 'compare mod-times with reduced accuracy',
    '--temp-dir': 'create temporary files in directory DIR',
    '--fuzzy': 'find similar file for basis if no dest file',
    '--compare-dest': 'also compare received files relative to DIR',
    '--copy-dest': '... and include copies of unchanged files',
    '--link-dest': 'hardlink to files in DIR when unchanged',
    '--compress': 'compress file data during the transfer',
    '--compress-level': 'explicitly set compression level',
    '--skip-compress': 'skip compressing files with suffix in LIST',
    '--cvs-exclude': 'auto-ignore files in the same way CVS does',
    '--filter': 'add a file-filtering RULE',
    '--exclude': 'exclude files matching PATTERN',
    '--exclude-from': 'read exclude patterns from FILE',
    '--include': 'don\'t exclude files matching PATTERN',
    '--include-from': 'read include patterns from FILE',
    '--files-from': 'read list of source-file names from FILE',
    '--from0': 'all *from/filter files are delimited by 0s',
    '--protect-args': 'no space-splitting; wildcard chars only',
    '--address': 'bind address for outgoing socket to daemon',
    '--port': 'specify double-colon alternate port number',
    '--sockopts': 'specify custom TCP options',
    '--blocking-io': 'use blocking I/O for the remote shell',
    '--stats': 'give some file-transfer stats',
    '--human-readable': 'output numbers in a human-readable format',
    '--progress': 'show progress during transfer',
    '--itemize-changes': 'output a change-summary for all updates',
    '--out-format': 'output updates using the specified FORMAT',
    '--log-file': 'log what we\'re doing to the specified FILE',
    '--log-file-format': 'log updates using the specified FMT',
    '--password-file': 'read daemon-access password from FILE',
    '--list-only': 'list the files instead of copying them',
    '--bwlimit': 'limit I\/O bandwidth; KBytes per second',
    '--write-batch': 'write a batched update to FILE',
    '--only-write-batch': 'like --write-batch but w/o updating dest',
    '--read-batch': 'read a batched update from FILE',
    '--protocol': 'force an older protocol version to be used',
    '--iconv=CONVERT_SPEC': 'request charset conversion of filenames',
    '--checksum-seed': 'set block/file checksum seed (advanced)',
    '--ipv4': 'prefer IPv4',
    '--ipv6': 'prefer IPv6',
    '--version': 'print version number'
}

rsync_push_options = ['--checksum', '--recursive', '--verbose', '--links', '--times', '--compress', '--exclude={}'.format(repository.REPOSITORY_DIR), '--chmod=ugo=rwX', '--progress']

class SyncResult:
    '''an object containing all information about the sync'''

    def __init__(self, files = []):
        self._files = files

    def getFiles(self):
        return self._files

def prepOptions(options = []):
    fixed_options = []

    for option in options:
        if '{backup_dir}' in option:
            option = option.format(backup_dir = utils.urlPath(repository.REPOSITORY_BACKUP_DIR))

        if '{files_from}' in option:
            option = option.format(files_from = LATEST_FILE)

        if '{exclude_file}' in option:
            option = option.format(exclude_file = EXCLUDE_FILE)

        fixed_options = appendDistinct(fixed_options, option)

    return fixed_options

def appendDistinct(old_list = [], new_item = None):
    new_list = [] + old_list

    if new_item:
        if not new_item in new_list:
            new_list.append(new_item)

    return new_list

def push(local = '', remote = '', *args, **kwargs):
    '''push from local to remote'''

    if local and remote:
        options = [] + rsync_push_options
        #options = prepOptions(rsync_push_options)

        for arg, value in kwargs.iteritems():
            if arg in rsync_options.keys():
                options.append('{arg}={value}'.format(arg = arg, value = value))

        # exclude from '.ecxlude' file
        if os.path.isfile(os.path.join(utils.getCurrentWorkingDir(), EXCLUDE_FILE)):
            options.append('--exclude-from={exclude_file}')

        if '--latest' in args:
            paths = []
            latest_options = appendDistinct(options, '--dry-run')

            latest_cmd = filter(bool, ['rsync', '-e ssh'] + prepOptions(latest_options) + [utils.urlPath(local), utils.urlPath(remote)])

            popen = subprocess.Popen(latest_cmd, stdout = subprocess.PIPE)

            for line in popen.stdout:
                stripped_line = line.strip()

                if stripped_line:
                    #print stripped_line

                    if re.match(r'^[^\s]+?$', stripped_line):
                        paths.append(stripped_line)

            classified_paths = latest.classifyPaths(paths)

            filtered_paths = latest.filterPaths(paths, classified_paths)

            if repository.exists():
                try:
                    with open(LATEST_FILE, 'w') as outfile:
                        #outfile.writelines(filtered_paths)
                        for path in [p for p in filtered_paths if not p.endswith('/')]:
                            outfile.write('{}\n'.format(path))
                except Exception as e:
                    raise Exception('could not save .include. reason: {reason}'.format(reason = e.message))
                else:
                    options.append('--files-from={files_from}')

        if '--delete' in args:
            options = options + ['--delete-during', '--backup', '--backup-dir={backup_dir}']

        #if any(o for o in options if o.startswith('--include')):
        #    options = filter(lambda o: not o.startswith('--exclude'), options)

        push_cmd = filter(bool, ['rsync', '-e ssh'] + prepOptions(options) + [utils.urlPath(local), utils.urlPath(remote)])

        if '--debug' in args:
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

def pull(local = '', remote = '', *args, **kwargs):
    '''pull from remote to local'''

    return push(remote, local, *args, **kwargs)

def diff():
    '''get diff from local to remote'''
    pass
