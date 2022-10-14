# fair-data-eeg
Repository for FairData society and EEG data

This repository serves as a proof of work that  we (Braintrip) have done to achieve a certain milestone which was set and agreed upon by both parties.

First we needed to familiarize ourselves with the whole principle of decentralized storage which includes using swarm and setting up a bee node in order to upload
files. But because that proces is time consuming, we opted for using gateway method for uploading the EEG recordings. Secondly we tried uploading a single EEG 
recording using said method, which was in BrainVision format. It consists of three files: eeg data file, header file and markers file. Files were archived in
zip format.

We used a FairOs gateway for uploading the EEG recording. The upload procedure is quite straightforward. In a terminal window we need to create a user,
then sign in and at last upload an EEG recording. Commands used for said operations are listed below. When you successfully create a new user you get an address
hash and a mnemonic.

#### Creating a user:

`curl 'https://fairosfairdatasociety.org/v1/user/signup' -H 'Content-Type: application/json' -d '{"user_name":"brainTrip","password":"verySafePassword"}'`

#### Login with created username and password: 

`curl 'https://fairos.fairdatasociety.org/v1/user/login' -H 'Content-Type: application/json' -d '{"user_name":"brainTrip","password":"verySafePassword"}'`

#### Upload command: 

`curl -i -X POST -H "Content-Type:application/zip" -T "./testEEG.zip" 'https://gateway.fairdatasociety.org.bzz'`

After a successful upload we get a message with an etag (some kind of hash), which can be used to download the file using the following command:
`curl -i -X GET 'https://gateway.fairdatasociety.org/bzz/insert_your_etag_between these_backslashes/'`

Etag access for uploaded EEG recording: `c2edca62a74aa225a1c8933c26147c072966367059587936e9021564811b407`

## Using the script for uploading

Firstly prepare the files which you intend to upload and put them in a folder. Then run `upload_dir.py` and if successful, the script will generate
a csv table, named : "fileType_etag_timestamp". It has three columns; file name, timestamp, etag. The table is intended to give other users access to 
uploaded files. 

The `upload_dir.py` script takes 4 arguments: 
- username,
- password, 
- path to the directory where the files are, 
- file type, which has the information what kind of files we want to upload and in which format (e.g. eegRecording/zip --> note: there can be other files in the 
folder, but the script will pick out only the ones with extension .zip)

#### Example of script usage: 
`python upload_dir.py username password C:\path\to\upload\folder eegRecording/zip`

Table of etags of uploaded EEG recordings can be found [here](https://github.com/BrainTrip/fair-data-eeg/tree/main/EEG_recordings).

## Additional notes

During uploading of files we found out, that the actual upload is quite fast, but it usually takes 4-6 minutes to recieve a response with an etag.
This method of upload is therefore not suitable for uploading big amounts of files.
