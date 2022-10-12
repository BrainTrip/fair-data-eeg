import sys
import subprocess
from os import listdir
import csv
from datetime import datetime

def login(username, password):
    try:
        command = 'curl "https://fairos.fairdatasociety.org/v1/user/login" -H "Content-Type: application/json" -d' \
                  ' "{\\\"user_name\\\":\\\"' + username + '\\\",\\\"password\\\":\\\"' + password + '\\\"}"'

        proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()

        print(stdout)
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
                date = string[string.find('Date:')+6:string.find('Date:')+35]
                etag = string[string.find('etag:')+7:string.find('etag:')+71]
                name = fileNames[i]
                etag_list.append([name, date, etag])

            # write etags to csv file
            fileName = type + '_etags_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
            with open(fileName, 'w', newline='') as etag:
                csv.writer(etag).writerows(etag_list)
    except Exception as e:
        print(stderr)
        print(e)


if __name__ == "__main__":
    if (login('brainTrip', 'CRAPEsEMstIC')):
        get_files_from_dir("C:\\Users\\jakak\\Desktop\\Jaka\\BrainTrip\\BDIapp\\fair-data-eeg\\EEG_recordings", 'textFile/txt')
