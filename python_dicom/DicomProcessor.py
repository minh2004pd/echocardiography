from DicomFileWriter import DicomFileWriter
from DicomClientServer import DicomClientServer
import threading
import time
import pydicom
import os
from io import BytesIO

class DicomProcessor:
    def __init__(self, session, base_url, auth):
        self.session = session
        self.base_url = base_url
        self.auth = auth
        self.dicom_client = DicomClientServer(session, base_url, auth)
        self.dicom_filewriter = DicomFileWriter()
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def process_study(self, study, name):
        series_list = self.dicom_client.get_series(study)
        for series in series_list:
            self.process_series(series, name)

    def process_series(self, series, name):
        instances = self.dicom_client.get_instances(series)
        for instance in instances:
            self.process_instance(instance, name)

    def process_instance(self, instance, name):
        dicom_file_data = self.dicom_client.get_dicom_file_data(instance)
        if dicom_file_data is not None:
            self.dicom_filewriter.write_dicom_file_data(dicom_file_data, name, instance['MainDicomTags']['InstanceNumber'])
        else:
            print('ERROR!!!')
    
    def process_instanceID(self, instanceID):
        instance = self.dicom_client.get_instance_by_ID(instanceID)
        dicom_file_data = self.dicom_client.get_dicom_file_data(instance)
        if dicom_file_data is not None:
            self.dicom_filewriter.write_dicom_file_data1(dicom_file_data, "new_file", instance['MainDicomTags']['InstanceNumber'])
        else:
            print('ERROR!!!')
    
    def process_instanceIDs(self, instanceIDs):
        for instanceID in instanceIDs:
            instance = self.dicom_client.get_instance_by_ID(instanceID)
            dicom_file_data = self.dicom_client.get_dicom_file_data(instance)
            if dicom_file_data is not None:
                ds = pydicom.dcmread(BytesIO(dicom_file_data))
                sop_instance_uid = ds.SOPInstanceUID
                found_in_file = False
                with open(os.path.join(self.root_dir, 'handled_id.txt'), 'r') as f:
                    for line in f:
                        if sop_instance_uid in line:
                            print("YES")
                            found_in_file = True
                            break
                if not found_in_file:
                    self.dicom_filewriter.write_dicom_file_data1(dicom_file_data, "new_file", instance['MainDicomTags']['InstanceNumber'])
            else:
                print('ERROR!!!')
    
    def process_count_instance(self, series):
        return len(series['Instances'])
    
    def get_number_studies(self):
        return len(self.dicom_client.get_studies)
    
    def get_list_instances(self):
        data = self.dicom_client.get_changes()
        # Extract the 'Changes' list from the response
        changes = data.get('Changes', [])
    
        cur_instances = [change.get('ID') for change in changes if change.get('ChangeType') == 'NewInstance']
        return cur_instances
    

