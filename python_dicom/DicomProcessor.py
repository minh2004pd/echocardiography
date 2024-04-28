from DicomFileWriter import DicomFileWriter
from DicomClientServer import DicomClientServer
import threading
import time

class DicomProcessor:
    def __init__(self, session, base_url, auth):
        self.session = session
        self.base_url = base_url
        self.auth = auth
        self.dicom_client = DicomClientServer(session, base_url, auth)
        self.dicom_filewriter = DicomFileWriter()

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
    
    def process_new_instances(self, instances):
        for instance in instances:
            dicom_file_data = self.dicom_client.get_dicom_file_data(instance)
            if dicom_file_data is not None:
                self.dicom_filewriter.write_dicom_file_data(dicom_file_data, "new_file", instance['Seq'])
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
    
        cur_instances = [change for change in changes if change.get('ChangeType') == 'NewInstance']
        return cur_instances
    
