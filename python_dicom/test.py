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
import queue
import threading
from collections import defaultdict
import os
import glob

path_to_dicoms_dir = Path('D:\\OneDrive\\Máy tính\\python_dicom\\dicom_files_import\\new_file_dicom')

path_to_dicoms_dir1 = Path('D:\\OneDrive\\Máy tính\\python_dicom\\dicom_files_import\\new_file')

base_url = 'http://localhost:8042'

username = 'orthanc'
password = 'orthanc'
auth = (username, password)

my_session = requests.session()

dicom_manager = DicomManager(my_session, base_url, auth)
last_content = "0"

start_time = time.time()

def reset_dir(path_to_dicoms_dir):
    # Get a list of all the file paths that ends with .dcm from in specified directory
    fileList = glob.glob(str(path_to_dicoms_dir / '*'))

    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)

while True:
    with open('D:/OneDrive/Máy tính/python_dicom/instance_ids.txt', 'r') as f:
        cur_content = f.read().replace(' ', '').replace('\n', '').replace('\t', '')

    if cur_content == '':
        continue
    elif cur_content != last_content:  # Check the uploading flag
        print(cur_content)
        dicom_manager.get_new_instance(cur_content)
        last_content = cur_content
        start_time = time.time()  # Reset start time when new content is found
    else:
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        if elapsed_time >= 3:  # If 3 seconds have passed, reset start time
            dicom_manager.handle_new_instance()
            dicom_manager.upload_all_dicom_files(path_to_dicoms_dir)
            
            reset_dir(path_to_dicoms_dir)
            reset_dir(path_to_dicoms_dir1)
            
            with open('D:/OneDrive/Máy tính/python_dicom/instance_ids.txt', 'w') as f:
                pass
            start_time = time.time()











