# INTERACTION WITH PACS
Welcome to the INTERACTION WITH PACS repository. This project provides an easy way to interact with PACS via Rest API

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/minh2004pd/echocardiography
   ```
## How to run the pipeline auto-detect new file upload, handle it, and push it back to the server
## To begin with, you need to launch the Orthanc server on Docker and use Python plugin for Orthanc.
```
docker run -p 4242:4242 -p 8042:8042 --rm ^
  -v "path\to\orthanc.json:/etc/orthanc/orthanc.json:ro" ^
  -v "path\to\python_dicom:/app" ^
  -v "path\to\hello.py:/etc/orthanc/hello.py:ro" ^
  jodogne/orthanc-python
```
## ```-p 4242:4242 -p 8042:8042``` maps ports from the host system to the container.
```
-v "path\to\orthanc.json:/etc/orthanc/orthanc.json:ro"
```
mounts the orthanc.json file from your local system to the container.

orthanc.json that contains the following minimal configuration for Orthanc:
```
{
  "StorageDirectory" : "/var/lib/orthanc/db",
  "RemoteAccessAllowed" : true,
  "Plugins" : [
    "/usr/local/share/orthanc/plugins"
  ],
  "PythonScript" : "/etc/orthanc/hello.py"
}
```
```
-v "path\to\python_dicom:/app"
```
mounts the entire python_dicom directory to the /app directory inside the container.
```
-v "path\to\hello.py:/etc/orthanc/hello.py:ro"
```
mounts the hello.py file to the /etc/orthanc/hello.py path in the container

Now when you run the command successfully, the ```hello.py``` file will run on container Orthanc-Python and interact with the current project file (remote interaction because of using mount) making event listening and handling new files uploaded to the Orthanc server

## Next, run the ```pipeline.py``` file to listen to new file uploads and handle them.

To test the functionality, you can run the file ```upload_dicom.py``` to upload some DICOM file to the server.

(Note that you must run the above 2 files in 2 separate processes)
