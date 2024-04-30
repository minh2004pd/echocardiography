import requests
import uuid
import hashlib
import pydicom
from pathlib import Path
from pydicom.filebase import DicomBytesIO
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests_toolbelt as tb
from io import BytesIO
import matplotlib.pyplot as plt
from DicomManager import DicomManager
import json
from pprint import pprint
import time


path_to_dicoms_dir = Path('D:\OneDrive\Máy tính\python_dicom\dicom_files')

base_url = 'http://localhost:8042'

username = 'orthanc'
password = 'orthanc'
auth = (username, password)

my_session = requests.session()

dicom_manager = DicomManager(my_session, base_url, auth)
last_content = "0"

instanceID = "9a1428e2-3420b7ba-1c7e9018-b4708dfe-60667edb"

# response = my_session.get(f'{base_url}/instances/{instanceID}/', auth=auth)
# print(response.json())

dicom_manager.upload_all_dicom_files(path_to_dicoms_dir)
# dicom_manager.get_all_studies()
# dicom_manager.get_studies_by_name('TCGA-CS-5396')








