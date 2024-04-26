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
import os

path_to_dicoms_dir = Path('D:\OneDrive\Máy tính\python_dicom\dicom_files')

base_url = 'http://localhost:8042'

username = 'orthanc'
password = 'orthanc'

client = requests.session()


# Create the URL for the instance
url = f'{base_url}/studies'

headers = {'Accept':'multipart/related; type="application/octet-stream"; transfer-syntax=*'}

response = client.get(url, headers=headers, auth=(username, password))

# Define the base URL of the Orthanc server
base_url = 'http://localhost:8042'

# Send a GET request to the Orthanc server to get a list of all studies
response = requests.get(url, auth=(username, password))

def get_series(study):
    response = requests.get(f'{base_url}/studies/{study}/series', auth=(username, password))
    return response.json()

def get_instances(series):
    response = requests.get(f'{base_url}/series/{series["ID"]}/instances', auth=(username, password))
    return response.json()

def get_dicom_file_data(instance):
    response = requests.get(f'{base_url}/instances/{instance["ID"]}/file', auth=(username, password))
    if response.status_code == 200:
        return response.content
    else:
        return None

def get_study_name(study):
    response = requests.get(f'{base_url}/studies/{study}', auth=(username, password))
    # print("Status code:", response.status_code)
    # print("Response data:", response.json())
    if response.status_code == 200:
        return response.json().get('PatientMainDicomTags').get('PatientName')
    else:
        return None

def write_dicom_file_data(dicom_file_data, name, number):
    directory = f'dicom_files_import/{name}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, f'{number}.dcm'), 'wb') as file:
        file.write(dicom_file_data)

def get_all_studies(studies):
    for study in studies:
        series_list = get_series(study)
        name = get_study_name(study)
        for series in series_list:
            instances = get_instances(series)
            for instance in instances:
                dicom_file_data = get_dicom_file_data(instance)
                if dicom_file_data is not None:
                    write_dicom_file_data(dicom_file_data, name, instance['MainDicomTags']['InstanceNumber'])

def get_studies_by_name(studies, name):
    for study in studies:
        study_name = get_study_name(study)
        if study_name == name:
            series_list = get_series(study)
            for series in series_list:
                instances = get_instances(series)
                for instance in instances:
                    dicom_file_data = get_dicom_file_data(instance)
                    if dicom_file_data is not None:
                        write_dicom_file_data(dicom_file_data, name, instance['MainDicomTags']['InstanceNumber'])

# Check if the request was successful
if response.status_code == 200:
    # The request was successful
    # The response body contains a list of all studies
    studies = response.json()
    #get_studies_by_name(studies, 'TCGA-CS-5396')
    get_all_studies(studies)

    print("DICOM files retrieved successfully!")
else:
    # The request failed
    print("Failed to retrieve DICOM files. Status code:", response.status_code)