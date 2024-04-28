import pydicom
from pydicom.filebase import DicomBytesIO
from requests_toolbelt.multipart.encoder import MultipartEncoder

class DicomUploader:
    def __init__(self, session, base_url, auth):
        self.session = session
        self.base_url = base_url
        self.auth = auth
    
    def upload_dicom_file(self, filepath):
        # Read the DICOM file with pydicom
        dataset = pydicom.dcmread(filepath)

        # Convert the DICOM dataset to bytes
        with DicomBytesIO() as f:
            dataset.save_as(f, write_like_original=True)
            rawfile = f.parent.getvalue()

        # Create a MultipartEncoder object
        multipart_data = MultipartEncoder(
            fields={
                'file': ('dicomfile', rawfile, 'application/dicom')
            }
        )

        headers = {'Accept':'application/dicom+json', "Content-Type": multipart_data.content_type}

        url = f'{self.base_url}/instances'
        response = self.session.post(url, data=multipart_data, headers=headers, verify=False, auth=self.auth)
        if response.status_code != 200:
            print(f'Error uploading {filepath}! Status code:', response.status_code)
            print('Response:', response.text)
        else:
            print(f'Successfully uploaded {filepath}!')
    
    def upload_all_dicom_files(self, dicom_dir):
        # Loop over all DICOM files in the directory
        for filepath in dicom_dir.glob('*.dcm'):
            self.upload_dicom_file(filepath)