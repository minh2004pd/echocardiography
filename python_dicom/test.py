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
import sseclient
import json
from pprint import pprint

path_to_dicoms_dir = Path('D:\OneDrive\Máy tính\python_dicom\dicom_files')

base_url = 'http://localhost:8042'

username = 'orthanc'
password = 'orthanc'
auth = (username, password)

my_session = requests.session()

# Create the URL for the instance
url = f'{base_url}/changes/'
response  = my_session.get(url, auth=auth)

dicom_manager = DicomManager(session=my_session, base_url=base_url, auth=auth)

# data = response.json()
# # Extract the 'Changes' list from the response
# changes = data.get('Changes', [])

# cur_instances = [change for change in changes if change.get('ChangeType') == 'NewInstance']
# for instance in cur_instances:
#     pprint(instance["ID"])





