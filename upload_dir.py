#! /usr/bin/env python

import sys
import subprocess
from os import listdir
import csv
from datetime import datetime
import re

def login(username, password):
    try:
        command = 'curl "https://fairos.fairdatasociety.org/user/login" -H "Content-Type: application/json" -d' \
                  ' "{\\\"user_name\\\":\\\"' + username + '\\\",\\\"password\\\":\\\"' + password + '\\\"}"'

        proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        print(stdout)
        returnString = stdout.decode('utf-8')
        if (returnString.find('200') == -1):
            return False
        return True
    except Exception as e:
        print(stderr)
        print(e)
        return False


def get_files_from_dir(dir, fileType):
    extension = '.' + fileType.split('/')[1]
    type = fileType.split('/')[0]
    fileNames = [f for f in listdir(dir) if f.endswith(extension)]
    onlyfiles = [dir + '\\' + f for f in listdir(dir) if f.endswith(extension)]
    # remove double \\
    paths = [f.replace('\\', '/') for f in onlyfiles]
    etag_list = [['file name', 'timestamp', 'etag']]
    err_count = 0
    try:
        if len(paths) == 0:
            print("There isn't any file with extension: %s" %extension)
        else:
            for i in range(len(paths)):
                command = 'curl -i -X POST -H "Content-Type:' + fileType + '" -T "' \
                + paths[i] + '" "https://gateway.fairdatasociety.org/bzz"'
                proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                stdout, stderr = proc.communicate()
                string = stdout.decode("utf-8")
                print(string)
                date = string[string.find('Date:')+6:string.find('Date:')+35]
                etag = string[string.find('etag:')+7:string.find('etag:')+71]
                name = fileNames[i]

                # check if the file was correctly uploaded and got an etag correct response
                if len(etag) == 64 and bool(re.match("^[a-zA-Z0-9]*$", etag)):
                    etag_list.append([name, date, etag])
                else:
                    err_count += 1

                if err_count >= 5:
                    print('There has been to many failed attempts at uploading a file.')
                    sys.exit()
            # write etags to csv file
            fileName = type + '_etags_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
            with open(fileName, 'w', newline='') as etag:
                csv.writer(etag).writerows(etag_list)
    except Exception as e:
        print(stderr)
        print(e)


if __name__ == "__main__":
    get_files_from_dir(sys.argv[1], sys.argv[2])
