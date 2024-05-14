import os

class DicomFileWriter:
    def write_dicom_file_data(self, dicom_file_data, name, number):
        # Get the directory of the current script
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        directory = os.path.join(root_dir, 'dicom_files_dowload')
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, f'{number}.dcm'), 'wb') as file:
            file.write(dicom_file_data)
    
    def write_dicom_file_data1(self, dicom_file_data, name, number):
        # Get the directory of the current script
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        directory = os.path.join(root_dir, 'dicom_files_import', name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, f'{number}.dcm'), 'wb') as file:
            file.write(dicom_file_data)