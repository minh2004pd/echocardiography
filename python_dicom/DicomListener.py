import requests
from pathlib import Path
import json
from pprint import pprint
import time
import threading
import os
import glob
import pydicom
from DicomProcessor import DicomProcessor
from io import BytesIO

class DicomListener:
    def __init__(self, session, base_url, auth, dicom_manager):
        self.path_to_dicoms_dir_handled = Path('.\\dicom_files_import\\new_file_dicom')
        self.path_to_dicoms_dir_new_file = Path('.\\dicom_files_import\\new_file')
        self.auth = auth
        self.session = session
        self.base_url = base_url
        self.dicom_manager = dicom_manager
        self.last_content = "0"
        self.start_time = time.time()
        self.dicom_processor = DicomProcessor(session, base_url, auth)

    def reset_dir(self, path_to_dicoms_dir):
        fileList = glob.glob(str(path_to_dicoms_dir / '*'))
        for filePath in fileList:
            try:
                os.remove(filePath)
            except:
                print("Error while deleting file : ", filePath)
    
    def check(self, difference):
        for id in difference:
            instance = self.dicom_client.get_instance_by_ID(id)
            dicom_file_data = self.dicom_client.get_dicom_file_data(instance)
            ds = pydicom.dcmread(BytesIO(dicom_file_data))
            sop_instance_uid = ds.SOPInstanceUID

    def listen(self):
        while True:
            last_check = self.dicom_processor.get_list_instances()
            while True:
                time.sleep(3)
                current_check = self.dicom_processor.get_list_instances()
                if last_check is not None and current_check is not None:
                    if len(current_check) > len(last_check):
                        print(f"New DICOM file(s) have been uploaded to the server. {len(current_check) - len(last_check)}")
                        difference = [item for item in current_check if item not in last_check]
                        self.dicom_processor.process_instanceIDs(difference)
                    else:
                        pass
                        # print("No New")
                last_check = current_check
    def set_path_to_dicoms_dir_handled(self, path):
        self.path_to_dicoms_dir_handled = path

    def set_path_to_dicoms_dir_new_file(self, path):
        self.path_to_dicoms_dir_new_file = path

    def get_path_to_dicoms_dir_handled(self):
        return self.path_to_dicoms_dir_handled
    
    def get_path_to_dicoms_dir_new_file(self):
        return self.path_to_dicoms_dir_new_file