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
import os

# Get the directory of the current script
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


path_to_dicoms_dir = Path(os.path.join(root_dir, 'dicom_files'))

base_url = 'http://localhost:8042'

username = 'orthanc'
password = 'orthanc'
auth = (username, password)

my_session = requests.session()

dicom_manager = DicomManager(my_session, base_url, auth)

dicom_manager.start_listening()

# dicom_manager.upload_all_dicom_files(path_to_dicoms_dir)
# dicom_manager.get_all_studies()
# dicom_manager.get_studies_by_name('TCGA-CS-5396')







