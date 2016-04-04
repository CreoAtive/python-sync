# python
import os
import re
import itertools

def printList(l = []):
    for i in l:
        print i

def getPaths(path = ''):
    '''recursively generate a list of paths'''

    exclude_paths = ['.repository']
    paths = []

    if os.path.isdir(path):
        #paths = [os.path.join(path, f) for f in os.listdir(path) if f not in exclude_paths]

        for name in os.listdir(path):
            current_path = os.path.join(path, name)

            if os.path.isfile(current_path):
                paths.append(current_path)

            if os.path.isdir(current_path):
                paths.append(current_path)

                paths += getPaths(current_path)

    return paths

def classifyPaths(paths = []):
    '''classify paths based on their version, extension and type (file / dir)'''

    classified_paths = []

    for path in paths:
        classify_match = re.match(r'^(.+?_v\d{3}_[\w\d\.\-_]+)(.*?)$', path)

        if classify_match:
            head = classify_match.group(1)
            tail = classify_match.group(2)

            root, extension = os.path.splitext(head)

            if not extension:
                extension = 'dir'

            key_match = re.match(r'^(.+?_v)(\d{3})_(.+?)$', head)

            if key_match:
                key = key_match.group(1)
                version = int(key_match.group(2))

                matching_paths = [path for index, path in enumerate(classified_paths) if path['key'] == key and path['extension'] == extension]

                if not matching_paths:
                    '''append path'''
                    classified_paths.append({
                        'extension': extension,
                        'key': key,
                        'path': head,
                        'version': version
                    })
                else:
                    matching_path = matching_paths[0]

                    if matching_path['version'] < version:
                        '''update path to latest version'''
                        matching_path['version'] = version
                        matching_path['path'] = head

    return classified_paths

def filterPaths(paths = [], classified_paths = []):
    '''filter paths based on classified paths'''

    filtered_paths = []

    for path in paths:
        classify_match = re.match(r'^(.+?_v\d{3}_[\w\d\.\-_]+)(.*?)$', path)

        if classify_match:
            '''check if path matches classified path'''

            if any(p['path'] for p in classified_paths if path.startswith(p['path'])):
                filtered_paths.append(path)
        else:
            '''append unclassified path'''
            filtered_paths.append(path)

    return filtered_paths

def main():
    paths = getPaths('D:/sync/cg/onTheHunt')

    classified_paths = classifyPaths(paths)

    filtered_paths = filterPaths(paths, classified_paths)

    for path in filtered_paths:
        print path

if __name__ == '__main__':
    main()
