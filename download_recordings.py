#! /usr/bin/env python

import sys
from clint.textui import progress
from os import listdir, makedirs, path
import pandas as pd
import requests


def download_files_from_csv(target_dir='downloaded_EEGs', files='-af', index='-ai'):
    if not path.isdir("./" + target_dir):
        print('creating dir')
        makedirs("./" + target_dir)
    if files == '-af':
        csvFiles = listdir('./EEG_recordings/')
    else:
        csvFiles = files.split(',')
    for file in csvFiles:
        df = pd.read_csv('./EEG_recordings/' + file)
        try:
            if index == '-ai':
                indexes = df.index
            else:
                indexes = index.split(',')
                indexes = [eval(i) for i in indexes]
            for ind in indexes:
                url = "https://gateway.fairdatasociety.org/bzz/"
                url += df['etag'][ind] + "/"

                r = requests.get(url, stream=True)

                with open("./downloaded_EEGs/" + df['file name'][ind], 'wb') as f:
                    total_length = int(r.headers.get('decompressed-content-length'))
                    print('downloading: ' + df['file name'][ind])
                    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                        if chunk:
                            f.write(chunk)
                            f.flush()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        download_files_from_csv(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('Not enough parameters')
