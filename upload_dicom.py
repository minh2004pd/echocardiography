import requests
import pydicom
from pathlib import Path
from pydicom.filebase import DicomBytesIO
from requests_toolbelt.multipart.encoder import MultipartEncoder

path_to_dicoms_dir = Path('D:\OneDrive\Máy tính\python_dicom\dicom_files_import\ACRIN-FLT-Breast_029')

base_url = 'http://localhost:8042'

client = requests.session()

url= f'{base_url}/instances'

response = client.get(url, auth=('orthanc', 'orthanc'))
if (response.status_code != 200):
    print('Error! Likely not authenticated!')
else: 
    print('authenticated!')

# Loop over all DICOM files in the directory
for filepath in path_to_dicoms_dir.glob('*.dcm'):
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

    url = f'{base_url}/instances'
    response = requests.post(url, data=multipart_data, headers=headers, verify=False, auth=('orthanc', 'orthanc'))
    if response.status_code != 200:
        print(f'Error uploading {filepath}! Status code:', response.status_code)
        print('Response:', response.text)
    else:
        print(f'Successfully uploaded {filepath}!')