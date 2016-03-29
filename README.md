# python-sync

A little package to mimic git-like-syncing-behaviour for large binary files with python and rsync. Deleted files will be moved to .repository/backups/<date>.

## init repository

Initialize empty repository in current working directory.

```
python pysync.py init
```

## clone repository

Clone from a remote repository.

```
python pysync.py clone <remote-ssh-url>
```

## pull repository

After cloning a repository or setting a remote origin you can pull changes from the remote repository.

```
python pysync.py pull
```

## push repository

Push changes to a remote origin.

```
python pysync.py push origin
```

## set remote origin

Set or change a remote origin url.

```
python pysync.py set-remote <origin> <remote-ssh-url>
```

## remove remote origin

Remove origin.

```
python pysync.py remove-remote <origin>
```
