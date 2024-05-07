import requests
from pathlib import Path
from DicomManager import DicomManager

path_to_dicoms_dir = Path('.\\dicom_files_import\\new_file_dicom')

path_to_dicoms_dir1 = Path('.\\dicom_files_import\\new_file')

base_url = 'http://localhost:8042'

username = 'orthanc'
password = 'orthanc'
auth = (username, password)

my_session = requests.session()

dicom_manager = DicomManager(my_session, base_url, auth)
dicom_manager.start_listening()













