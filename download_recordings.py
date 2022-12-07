import sys
import subprocess
from os import listdir
import pandas as pd
from datetime import datetime
import re


def download_files_from_csv(files='-af', index='-ai'):
    # if user doesn't specify a file it is assumed that the whole folder will be downloaded
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
                command = 'curl -X GET "https://gateway.fairdatasociety.org/bzz/'
                command += df['etag'][ind] + '/" -o ' + df['file name'][ind]
                proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                stdout, stderr = proc.communicate()
        except Exception as e:
            print('Arguments used were not correct, please check arguments instruction in readme file.')


if __name__ == "__main__":
    param1, param2 = '-af', '-ai'
    if len(sys.argv) > 2:
        param1, param2 = sys.argv[1], sys.argv[2]
    elif len(sys.argv) > 1:
        param1 = sys.argv[1]

    download_files_from_csv(param1, param2)

