import requests
from pathlib import Path
import json
from pprint import pprint
import time
import threading
import os
import glob

class DicomListener:
    def __init__(self, session, base_url, auth, dicom_manager):
        self.path_to_dicoms_dir = Path('.\\dicom_files_import\\new_file_dicom')
        self.path_to_dicoms_dir1 = Path('.\\dicom_files_import\\new_file')
        self.auth = auth
        self.session = session
        self.base_url = base_url
        self.my_session = requests.session()
        self.dicom_manager = dicom_manager
        self.last_content = "0"
        self.start_time = time.time()

    def reset_dir(self, path_to_dicoms_dir):
        fileList = glob.glob(str(path_to_dicoms_dir / '*'))
        for filePath in fileList:
            try:
                os.remove(filePath)
            except:
                print("Error while deleting file : ", filePath)

    def listen(self):
        while True:
            with open('.\\instance_ids.txt', 'r') as f:
                cur_content = f.read().replace(' ', '').replace('\n', '').replace('\t', '')

            if cur_content == '':
                continue
            elif cur_content != self.last_content:
                print(cur_content)
                self.dicom_manager.get_new_instance(cur_content)
                self.last_content = cur_content
                self.start_time = time.time()
            else:
                elapsed_time = time.time() - self.start_time
                if elapsed_time >= 3:
                    self.dicom_manager.handle_new_instance()
                    self.dicom_manager.upload_all_dicom_files(self.path_to_dicoms_dir)
                    self.reset_dir(self.path_to_dicoms_dir)
                    self.reset_dir(self.path_to_dicoms_dir1)
                    with open('.\\instance_ids.txt', 'w') as f:
                        pass
                    self.start_time = time.time()