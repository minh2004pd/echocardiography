import os

class DicomFileWriter:
    def write_dicom_file_data(self, dicom_file_data, name, number):
        directory = f'dicom_files_import/{name}'
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, f'{number}.dcm'), 'wb') as file:
            file.write(dicom_file_data)