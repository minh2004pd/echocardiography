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
from DicomManager import DicomManager
import json
from pprint import pprint
import time
import os
from PIL import Image
import numpy as np
import datetime


# Get the directory of the current script
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


path_to_dicoms_dir = Path(os.path.join(root_dir, 'dicom_files'))

base_url = 'http://localhost:8042'

username = 'orthanc'
password = 'orthanc'
auth = (username, password)

my_session = requests.session()
response = my_session.get(f'{base_url}/changes?limit=100', auth=auth)
print(response.content)

# dicom_manager = DicomManager(my_session, base_url, auth)

# dicom_manager.start_listening()

# dicom_manager.upload_all_dicom_files(path_to_dicoms_dir)
# dicom_manager.get_all_studies()
# dicom_manager.get_studies_by_name('TCGA-CS-5396')

# def dicom_to_png(dicom_filepath, png_filepath):
#     # Load the DICOM image
#     ds = pydicom.dcmread(dicom_filepath)
#     # Convert DICOM image to numpy array
#     img = ds.pixel_array
#     # Normalize the image to 0-255
#     img = np.uint8((img - np.min(img)) / np.ptp(img) * 255)
#     # Convert numpy array to PIL image
#     img = Image.fromarray(img)
#     # Save the image in PNG format
#     img.save(png_filepath)

# def png2dicom(ds1, png_path, dcm_path):
#     # Read the PNG image and convert it to numpy array
#     im = Image.open(png_path)
#     arr = np.array(im)

#     # Create a DICOM dataset
#     ds = pydicom.dataset.FileDataset('', {}, file_meta=None, preamble=b'\x00'*128)

#     # Set the metadata fields
#     ds.PatientID = ds1.PatientID
#     ds.PatientBirthDate = ds1.PatientBirthDate
#     ds.PatientSex = ds1.PatientSex
#     ds.StudyDate = ds1.StudyDate
#     ds.AccessionNumber = ds1.AccessionNumber
#     ds.ReferringPhysicianName = ds1.ReferringPhysicianName
#     ds.StudyInstanceUID = ds1.StudyInstanceUID
#     ds.StudyID = ds1.StudyID
#     ds.RequestedProcedureDescription = ds1.RequestedProcedureDescription
#     ds.SeriesInstanceUID = pydicom.uid.generate_uid()
#     ds.InstanceNumber = ds1.InstanceNumber
#     ds.SOPInstanceUID = pydicom.uid.generate_uid()
#     ds.BodyPartExamined = ds1.BodyPartExamined
#     ds.Modality = ds1.Modality
#     ds.SamplesPerPixel = 3 if len(arr.shape) == 3 else 1
#     ds.PhotometricInterpretation = 'RGB' if len(arr.shape) == 3 else 'MONOCHROME2'
#     ds.Rows, ds.Columns = arr.shape[:2]
#     ds.PixelSpacing = [1, 1]
#     ds.BitsAllocated = 8
#     ds.BitsStored = 8
#     ds.HighBit = 7
#     ds.PixelRepresentation = 0
#     ds.RescaleIntercept = 0
#     ds.RescaleSlope = 1
#     ds.WindowCenter = [127, 127, 127] if len(arr.shape) == 3 else [127]
#     ds.WindowWidth = [255, 255, 255] if len(arr.shape) == 3 else [255]
#     ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
#     ds.PlanarConfiguration = 0

#     # Assign the pixel array
#     ds.PixelData = arr.tobytes()

#     # Save the DICOM file
#     ds.save_as(dcm_path)

# if __name__ == '__main__':
#     # Use the function
#     bn_name = "PatientID"  # Replace with actual patient ID
#     png_path = "D:\\OneDrive\\Máy tính\\python_dicom\\dicom_files_import\\new_file_dicom\\1-017.png"  # Replace with actual JPEG file path
#     dcm_path = "D:\\OneDrive\\Máy tính\\python_dicom\\dicom_files_import\\new_file\\1-020.dcm"  # Replace with actual DICOM file path
#     ds1 = pydicom.dcmread('D:\\OneDrive\\Máy tính\\python_dicom\\dicom_files\\1-017.dcm')
#     png2dicom(ds1, png_path, dcm_path)
#     dicom_manager.upload_dicom_file(Path(dcm_path))
#     dicom_manager.upload_dicom_file(Path('D:\\OneDrive\\Máy tính\\python_dicom\\dicom_files\\1-017.dcm'))







