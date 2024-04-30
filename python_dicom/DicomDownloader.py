from DicomClientServer import DicomClientServer
from DicomProcessor import DicomProcessor

class DicomDownloader:
    def __init__(self, session, base_url, auth):
        self.session = session
        self.base_url = base_url
        self.auth = auth
        self.dicom_client = DicomClientServer(session, base_url, auth)
        self.dicom_processor = DicomProcessor(session, base_url, auth)

    def is_study_name_match(self, study, name):
        return self.dicom_client.get_study_name(study) == name
    
    def get_studies_by_name(self, studies, name):
        for study in studies:
            if self.is_study_name_match(study, name):
                self.dicom_processor.process_study(study, name)

    def get_all_studies(self, studies):
        for study in studies:
            name = self.dicom_client.get_study_name(study)
            self.dicom_processor.process_study(study, name)
    
    def load_instance_by_ID(self, instanceID):
        self.dicom_processor.process_new_instance(instanceID)