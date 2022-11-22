# fair-data-eeg
## Table of Contents
- [About Braintrip](#about-braintrip)
- [Uploading/downloading a file using a terminal window](#uploading/downloading-a-file-using-a-terminal-window)
  - [List of Commands](#list-of-commands)
- [Using the upload script](#using-the-upload-script)
  - [Example of upload script usage](#example-of-upload-script-usage)
- [Using the download script](#using-the-download-script)
  - [Example of download script usage](#example-of-download-script-usage)
- [EEG recordings access](#eeg-recordings-access)
- [Additional notes](#additional-notes)

## About braintrip project

The BrainTrip project is attempting to use quantitative analysis of EEG data to predict cognitive decline and dementia in seniors. We've performed several hundred EEG recordings using a 24-channel EEG amplifier and saline sponge based EEG caps. Our EEG data is encoded in the BrainVision format. Each EEG recoring has 3 associated files: a binary raw EEG file (.egg), and two ascii files containing marker (.vmrk) and header (.vhdr) information about special events in the EEG (markers) and channel names and positions (header). 

Further information on BrainVision format are available [here](https://www.brainproducts.com/download/specification-of-brainvision-core-data-format-1-0/)

To prepare your EEG data for upload, please convert your raw files to the BrainVison format for ease of use across different labs. Then follow the upload instructions.

## Uploading/downloading a file using terminal window

There is no requirements in order to upload or download files by using the bee gateway. However, if you are using it for the first time, you need to create a user using a command provided in ***list of commands***. Otherwise, you only need to log in by typing a login command in the terminal window. 
#### Upload file
In order to upload a file you need to pass an upload command to a terminal window (shown below). A file should consist a header file, marker file and raw eeg, archived using 7zip software to a .zip file.

If the upload is successful you should get a response similar to this:

```
HTTP/1.1 201 Created
Server: nginx
Date: Thu, 27 Oct 2022 07:33:45 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 82
Connection: keep-alive
x-powered-by: Express
access-control-expose-headers: Swarm-Tag
etag: "469948072a5b62f382911293888fe960cb1e18160941282348e6f321b2aa076e"
swarm-tag: 567568429
swarm-server-id: gw_bee_be1
Access-Control-Allow-Methods: POST
Access-Control-Allow-Headers: *
```

The response consists of information about upload status, but the most important bit of information is the etag. This is a hash that was given to the uploaded file and is used in download command to access said file. 

### Important !!!

In order for other people to be able to access uploaded files, the etag should also be made available in this repo. It would be best to upload a csv table containing three rows: file name, timestamp, etag. The csv file should be named like this: 

`fileType + '_etag_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv'`.

Example: eegRecordings_etags_2022-10-04_10-23-24.csv

#### Download a file
To download a specific EEG recording, you need to log in and move to a desired directory via terminal window and execute a download command. The file should be downloaded in current directory under a specified name, which you write at the end of download command.

### List of commands:
- #### Creating a user:

  `curl 'https://fairosfairdatasociety.org/v1/user/signup' -H 'Content-Type: application/json' -d '{"user_name":"brainTrip","password":"verySafePassword"}'`

- #### Login with created username and password: 

  `curl 'https://fairos.fairdatasociety.org/v1/user/login' -H 'Content-Type: application/json' -d '{"user_name":"brainTrip","password":"verySafePassword"}'`

- #### Upload command: 

  `curl -i -X POST -H "Content-Type: eegRecordings/zip" -T "./testEEG.zip" 'https://gateway.fairdatasociety.org.bzz'`
  
- #### Download command:
  `curl -i -X GET 'https://gateway.fairdatasociety.org/bzz/insert_your_etag_between these_backslashes/' --output fileName.zip`

## Using the upload script

In order to upload files more easily, we wrote a simple upload script (`upload_dir.py`), which uploads specified type of files from the chosen directory to Swarm. 

Firstly, you need to prepare the files, which are intended for upload and put them in a desired directory. Prepare the eeg recordings in BrainVision format (header file, marker file and raw EEG) and archive them using 7-zip software to a .zip file. Then run `upload_dir.py` script which takes 4 arguments:  
- path to the directory where the .zip files are, 
- file type, which has the information what kind of files we want to upload and in which format (e.g. eegRecording/zip --> note: there can be other files in the 
folder, but the script will pick out only the ones with extension .zip) 

If the upload is successful, the script will generate a csv table, named by a formula: "fileType_etag_timestamp.csv". It has three columns; file name, timestamp, etag. The table is intended to give other users access to uploaded recordings. **The csv file should be uploaded to this repo in EEG_recordings folder.** 

#### Example of upload script usage: 
`python upload_dir.py C:\path\to\upload\folder eegRecording/zip`

## Using the download script
TODO: create a download script in the first place

#### Example of download script usage:

## EEG recordings access

Tables of etags of uploaded EEG recordings can be found [here](https://github.com/BrainTrip/fair-data-eeg/tree/main/EEG_recordings).

## Additional notes

You can also download the files using [this link.](https://gateway.fairdatasociety.org/)
