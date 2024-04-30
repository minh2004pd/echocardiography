from multiprocessing import Process, Queue
from DicomManager import DicomManager
import requests
from pathlib import Path
from queue import Empty

path_to_dicoms_dir = Path('D:/OneDrive/Máy tính/python_dicom/dicom_files')

base_url = 'http://localhost:8042'

username = 'orthanc'
password = 'orthanc'
auth = (username, password)

my_session = requests.session()

dicom_manager = DicomManager(session=my_session, base_url=base_url, auth=auth)

