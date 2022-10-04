# fair-data-eeg
Repository for FairData society and EEG data

This repository serves as a proof of work that  we (Braintrip) have done to achieve a certain milestone which was set and agreed upon by both parties.

First we needed to familiarize ourselves with the whole principle of decentralized storage which includes using swarm and setting up a bee node in order to upload
files. But because that proces is time consuming, we opted for using gateway method of uploading a EEG recordings. Secondly we tried uploading a single EEG recording
using said method, which was in BrainVision format. It consists of three files: eeg data file, header file and markers file.

We used Bee gateway for uploading the EEG recording. The upload procedure is quite straightforward. In a terminal window we needed to do was to creata a user,
then sign in with that user and at last upload an EEG recording. Commands used for said operations are in upload.bash file. When you create a user you get an address
hash and a mnemonic.

Creating a user:

`curl 'https://fairosfairdatasociety.org/v1/user/signup' -H 'Content-Type: application/json' -d '{"user_name":"brainTrip","password":"verySafePassword"}'`

Login with created username and password: 

`curl 'https://fairos.fairdatasociety.org/v1/user/login' -H 'Content-Type: application/json' -d '{"user_name":"brainTrip","password":"verySafePassword"}'`

Upload command: 

`curl -i -X POST -H "Content-Type:application/zip" -T "./testEEG.zip" 'https://gateway.fairdatasociety.org.bzz'`

After a successful upload we got a message with an etag (some kind of hash) which can be used to download the file using the following command:
`curl -i -X GET 'https://gateway.fairdatasociety.org/bzz/etag/'`

Etag access for uploaded EEG recording: `c2edca62a74aa225a1c8933c26147c072966367059587936e9021564811b407`

## Following steps

Our next steps are to upload 100 EEG recordings, using the API method. We will also post a .csv file containing etags to all uploaded files.
