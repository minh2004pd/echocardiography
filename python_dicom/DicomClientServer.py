class DicomClientServer:
    def __init__(self, session, base_url, auth):
        self.session = session
        self.base_url = base_url
        self.auth = auth
    
    def get_studies(self):
        response = self.session.get(f'{self.base_url}/studies', auth=self.auth)
        # Check if the request was successful
        if response.status_code == 200:
            # The request was successful
            return response.json()
        else:
            # The request failed
            print("Failed to retrieve DICOM files. Status code:", response.status_code)

    def get_series(self, study):
        response = self.session.get(f'{self.base_url}/studies/{study}/series', auth=self.auth)
        return response.json()

    def get_instances(self, series):
        response = self.session.get(f'{self.base_url}/series/{series["ID"]}/instances', auth=self.auth)
        return response.json()

    def get_dicom_file_data(self, instance):
        response = self.session.get(f'{self.base_url}/instances/{instance["ID"]}/file', auth=self.auth)
        if response.status_code == 200:
            return response.content
        else:
            return None

    def get_study_name(self, study):
        response = self.session.get(f'{self.base_url}/studies/{study}', auth=self.auth)
        if response.status_code == 200:
            return response.json().get('PatientMainDicomTags').get('PatientName')
        else:
            return None
    
    def get_changes(self):
        # Create the URL for the instance
        url = f'{self.base_url}/changes/'
        response = self.session.get(url, auth=self.auth)
        return response.json()