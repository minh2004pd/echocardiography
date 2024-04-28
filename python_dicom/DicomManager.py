from DicomUploader import DicomUploader
from DicomDownloader import DicomDownloader
from DicomClientServer import DicomClientServer
from DicomProcessor import DicomProcessor
import threading
import time
import asyncio
import websockets
import asyncio
from datetime import datetime

class DicomManager:
    def __init__(self, session, base_url, auth):
        self.session = session
        self.base_url = base_url
        self.auth = auth
        self.dicom_uploader = DicomUploader(session, base_url, auth)
        self.dicom_downloader = DicomDownloader(session, base_url, auth)
        self.dicom_client = DicomClientServer(session, base_url, auth)
        self.dicom_processor = DicomProcessor(session, base_url, auth)
        self.start_monitoring()
    
    def start_monitoring(self, check_interval=3):
        def monitor():
            last_check = self.dicom_processor.get_list_instances()
            while True:
                time.sleep(check_interval)
                current_check = self.dicom_processor.get_list_instances()
                if last_check is not None and current_check is not None:
                    if len(current_check) > len(last_check):
                        print(f"New DICOM file(s) have been uploaded to the server. {len(current_check) - len(last_check)}")
                        difference = [item for item in current_check if item not in last_check]
                        self.dicom_processor.process_new_instances(difference)
                    else:
                        print("No New")
                last_check = current_check

        monitoring_thread = threading.Thread(target=monitor)
        monitoring_thread.start()

    def upload_dicom_file(self, filepath):
        self.dicom_uploader.upload_dicom_file(filepath)

    def upload_all_dicom_files(self, dicom_dir):
        self.dicom_uploader.upload_all_dicom_files(dicom_dir)

    def get_studies_by_name(self, name):
        response = self.dicom_client.get_studies()
        
        # Check if the request was successful
        if response.status_code == 200:
            # The request was successful
            # The response body contains a list of all studies
            studies = response.json()
            self.dicom_downloader.get_studies_by_name(studies, name)

            print("DICOM files retrieved successfully!")
        else:
            # The request failed
            print("Failed to retrieve DICOM files. Status code:", response.status_code)

    def get_all_studies(self):
        response = self.dicom_client.get_studies()
        
        # Check if the request was successful
        if response.status_code == 200:
            # The request was successful
            # The response body contains a list of all studies
            studies = response.json()
            self.dicom_downloader.get_all_studies(studies)

            print("DICOM files retrieved successfully!")
        else:
            # The request failed
            print("Failed to retrieve DICOM files. Status code:", response.status_code)