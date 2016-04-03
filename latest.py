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

def latestPaths(paths = []):
    '''select latest version of path'''

    filtered_paths = []

    for path in paths:
        current_head, current_tail = os.path.split(path)
        current_root, current_ext = os.path.splitext(current_tail)
        path_match = re.match(r'(.*_v)(\d{3})_', path)

        if path_match:
            path_part = path_match.group(1)
            version = int(path_match.group(2))

            try:
                key = next(index for (index, d) in enumerate(filtered_paths) if d['path_part'] == path_part and d['extension'] == current_ext)

                #print '{}\n{}\n\n'.format(path, filtered_paths[key]['path'])
            except Exception:
                key = False

            #print version, current_tail

            #print key, current_tail

            if key:
                matched_item = filtered_paths[key]

                if version > matched_item['version']:
                    #print version, matched_item['version']

                    filtered_paths.pop(key)

            filtered_paths.append({
                'path': path,
                'version': version,
                'extension': current_ext,
                'path_part': path_part
            })

    return filtered_paths

def classifyPaths(paths = []):
    classified_paths = []

    for path in paths:
        path_match = re.match(r'^(.+?_v)(\d{3})_(.+?)$', path)
        classify_match = re.match(r'^(.+?_v\d{3}_[\w\d\.\-_]+)(.*?)$', path)

        if path_match and classify_match:
            key = path_match.group(1)
            version = int(path_match.group(2))
            tail = path_match.group(3)
            classified_path = classify_match.group(1)
            classified_tail = classify_match.group(2)

            root, extension = os.path.splitext(classified_path)

            if not extension or classified_tail:
                extension = 'dir'

                print classified_tail

            classified_paths.append({
                'path': classified_path,
                'key': key,
                'version': version,
                'extension': extension
            })

    return classified_paths

def groupedPaths(classified_paths = []):
    sorted_input = sorted(classified_paths, key = lambda k: k['path'])

    groups = {}

    for classified_path in classified_paths:
        if not classified_path['key'] in groups:
            groups[classified_path['key']] = {}

        if not classified_path['extension'] in groups[classified_path['key']]:
            groups[classified_path['key']][classified_path['extension']] = []

        groups[classified_path['key']][classified_path['extension']].append(classified_path['path'])

    return groups

    #groups = itertools.groupby(sorted_input, key = lambda k: k['key'])

    #return [{'key': k, 'paths': [x['path'] for x in v]} for k, v in groups]

def filteredPaths(paths = [], grouped_paths = []):
    filtered_paths = []

    for path in paths:
        current_head, current_tail = os.path.split(path)
        current_root, current_ext = os.path.splitext(current_tail)

        if current_ext:
            extension = current_ext
        else:
            extension = 'dir'

        matching_keys = [item for key, item in grouped_paths.iteritems() if path.startswith(key)]

        if matching_keys:
            matching_key = matching_keys[0]

            if extension in matching_key.keys():
                if not extension == 'dir':
                    latest_version = matching_key[extension][-1]

                    if not latest_version in filtered_paths:
                        filtered_paths.append(latest_version)
                else:
                    latest_version = matching_key[extension][-1]

                    #print latest_version

                    if path.startswith(latest_version):
                        if not path in filtered_paths:
                            filtered_paths.append(path)

                            print path

    quit()

    return filtered_paths

def main():
    paths = getPaths('/Users/bernhardesperester/sync/cg/onTheHunt')

    classified_paths = classifyPaths(paths)

    return

    grouped_paths = groupedPaths(classified_paths)

    filtered_paths = filteredPaths(paths, grouped_paths)

    for filtered_path in filtered_paths:
        print filtered_path

    return

    for group in grouped_paths:
        if group['key'] == '/Users/bernhardesperester/sync/cg/onTheHunt/assets/girl/cg-exchange/output-zbrush/sculpting_girl_v':
            print group['paths'][-2]

if __name__ == '__main__':
    main()
