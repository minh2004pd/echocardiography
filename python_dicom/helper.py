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
import json

def png2dicom(data, png_path, dcm_path):
    # Read the PNG image and convert it to numpy array
    im = Image.open(png_path)
    arr = np.array(im)

    # Create a DICOM dataset
    ds = pydicom.dataset.FileDataset('', {}, file_meta=None, preamble=b'\x00'*128)

    ds.PatientID = data['PatientID']
    ds.PatientBirthDate = data['PatientBirthDate']
    ds.PatientSex = data['PatientSex']
    ds.StudyDate = data['StudyDate']
    ds.AccessionNumber = data['AccessionNumber']
    ds.ReferringPhysicianName = data['ReferringPhysicianName']
    ds.StudyInstanceUID = data['StudyInstanceUID']
    ds.StudyID = data['StudyID']
    ds.RequestedProcedureDescription = data['RequestedProcedureDescription']
    ds.InstanceNumber = data['InstanceNumber']
    ds.BodyPartExamined = data['BodyPartExamined']
    ds.Modality = data['Modality']
    ds.SOPInstanceUID = data['SOPInstanceUID']

    # Set the remaining fields
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SamplesPerPixel = 3 if len(arr.shape) == 3 else 1
    ds.PhotometricInterpretation = 'RGB' if len(arr.shape) == 3 else 'MONOCHROME2'
    ds.Rows, ds.Columns = arr.shape[:2]
    ds.PixelSpacing = [1, 1]
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.RescaleIntercept = 0
    ds.RescaleSlope = 1
    ds.WindowCenter = [127, 127, 127] if len(arr.shape) == 3 else [127]
    ds.WindowWidth = [255, 255, 255] if len(arr.shape) == 3 else [255]
    ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    ds.PlanarConfiguration = 0

    # Assign the pixel array
    ds.PixelData = arr.tobytes()

    # Save the DICOM file
    ds.save_as(dcm_path)

def dicom_to_png(dicom_filepath, png_filepath):
    # Load the DICOM image
    ds = pydicom.dcmread(dicom_filepath)
    # Convert DICOM image to numpy array
    img = ds.pixel_array
    # Normalize the image to 0-255
    img = np.uint8((img - np.min(img)) / np.ptp(img) * 255)
    # Convert numpy array to PIL image
    img = Image.fromarray(img)
    # Save the image in PNG format
    img.save(png_filepath)