# fair-data-eeg
## Table of Contents
- [Information about data format](#information-about-data-format)
- [Uploading/downloading a file using a terminal window](#uploading/downloading-a-file-using-a-terminal-window)
  - [List of Commands](#list-of-commands)
- [Using the upload script](#using-the-upload-script)
  - [Example of upload script usage](#example-of-upload-script-usage)
- [Using the download script](#using-the-download-script)
  - [Example of download script usage](#example-of-download-script-usage)
- [EEG recordings access](#eeg-recordings-access)
- [Additional notes](#additional-notes)
## Information about data format

EEG recordings are in BrainVision format. The format consists of three separate files:
- Header file (\*.vhdr)
  This is a text file containing recording parameters and further meta-information. It has the same base name as the raw EEG data file.
- Marker file (\*.vmrk)
  This is a text file describing the events that have been collected during the EEG data recording. It has the same base name as the raw EEG data file.
- Raw EEG data file (\*.eeg)
  This is a binary file containing the EEG data as well as additional signals recorded along with the EEG.

Further information on BrainVision format are available [here](https://www.brainproducts.com/download/specification-of-brainvision-core-data-format-1-0/)

## Uploading/downloading a file using terminal window

There is no requirements in order to upload or download files by using the bee gateway. However, if you are using it for the first time, you need to create a user using a command provided in ***list of commands***. Otherwise, you only need to log in by typing a login command in the terminal window. In order to upload a file you need to pass an upload command to a terminal window (shown below). A file can be 

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

Firstly, you need to prepare the files, which are intended for upload and put them in a desired directory. The `upload_dir.py` script takes 4 arguments: 
- username,
- password, 
- path to the directory where the files are, 
- file type, which has the information what kind of files we want to upload and in which format (e.g. eegRecording/zip --> note: there can be other files in the 
folder, but the script will pick out only the ones with extension .zip) 

Then run `upload_dir.py` and if successful, the script will generate
a csv table, named : "fileType_etag_timestamp". It has three columns; file name, timestamp, etag. The table is intended to give other users access to 
uploaded files. 



#### Example of upload script usage: 
`python upload_dir.py username password C:\path\to\upload\folder eegRecording/zip`

## Using the download script
TODO: create a download script in the first place

#### Example of download script usage:

## EEG recordings access

Tables of etags of uploaded EEG recordings can be found [here](https://github.com/BrainTrip/fair-data-eeg/tree/main/EEG_recordings).

## Additional notes

During uploading of files we found out, that the actual upload is quite fast, but it usually takes 4-6 minutes to recieve a response with an etag.
This method of upload is therefore not suitable for uploading big amounts of files.
