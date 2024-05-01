import requests
import pydicom
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2 
import uuid
from pathlib import Path
from PIL import Image
from pydicom.uid import generate_uid

class DicomHandler:
    def __init__(self, session, base_url, auth):
        self.session = session
        self.auth = auth
        self.base_url = base_url
    
    def handle_dicom1(self, directory = '.\\dicom_files_import\\new_file', directory1 = ".\\dicom_files_import\\new_file_dicom"):
        # Generate a new Series Instance UID
        new_series_uid = generate_uid()
        for filename in os.listdir(directory):
            if filename.endswith(".dcm"):
                filepath = os.path.join(directory, filename)
                self.ds = pydicom.dcmread(filepath)
                pixel_data = self.ds.pixel_array

                line_start = (100, 100)  
                line_end = (400, 400)    
                thickness = 9           
                color = 255    

                line_image = np.zeros_like(pixel_data)
                cv2.line(line_image, line_start, line_end, color, thickness)

                pixel_data += line_image
                self.ds.PixelData = pixel_data.tobytes()
                # Change the Series Instance UID to save as a different series
                self.ds.SeriesInstanceUID = new_series_uid
                
                self.ds.save_as(os.path.join(directory1, f'{filename}_modified.dcm'))
                # os.remove(filepath)  # Delete the file

    def handle_dicom(self, directory = '.\\dicom_files_import\\new_file', directory1 = ".\\dicom_files_import\\new_file_dicom"):
        # Generate a new Series Instance UID
        new_series_uid = generate_uid()
        for filename in os.listdir(directory):
            if filename.endswith(".dcm"):
                filepath = os.path.join(directory, filename)
                self.ds = pydicom.dcmread(filepath)
                fig, ax = plt.subplots()
                ax.imshow(self.ds.pixel_array, cmap=plt.cm.bone)
                ax.plot([0, self.ds.Columns], [self.ds.Rows/2, self.ds.Rows/2])  # Vẽ một đường
                plt.savefig(os.path.join(directory, f'{filename}_modified.png'))
                plt.close()
                # Save the modified DICOM file
                # Open the modified image
                modified_image = Image.open(os.path.join(directory, f'{filename}_modified.png'))

                # Convert the image to grayscale
                modified_image = modified_image.convert('L')

                # Resize the image array to match the original DICOM image shape
                modified_image = modified_image.resize((self.ds.Columns, self.ds.Rows))

                # Convert the image to a numpy array and scale it to the original bit depth
                modified_image_array = np.array(modified_image) * (np.max(self.ds.pixel_array) / 255)

                # Update the pixel data in the DICOM dataset
                self.ds.PixelData = modified_image_array.astype(self.ds.pixel_array.dtype).tobytes()

                # Change the Series Instance UID to save as a different series
                self.ds.SeriesInstanceUID = new_series_uid

                self.ds.save_as(os.path.join(directory1, f'{filename}_modified.dcm'))
                # os.remove(filepath)  # Delete the file

# Sử dụng class
# handler = DicomHandler('your_instance_id')
# handler.download_dicom()
# handler.read_dicom()
# handler.edit_dicom()
# handler.save_edited_dicom()
# handler.upload_dicom()