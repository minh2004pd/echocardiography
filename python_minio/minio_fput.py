import pydicom
from minio import Minio
from minio.error import S3Error
import os

# Create a client with the MinIO server playground, its access key
# and secret key.
client = Minio("localhost:9010",
    access_key="minh2004pd",
    secret_key="05112004pd",
    secure=False
)

def fput_minio(local_image_url, filename):
    # The file to upload, change this path if needed
    source_file = local_image_url

    # Load the DICOM file
    ds = pydicom.dcmread(source_file)

    # Get the information
    modality = ds.Modality
    patient_id = ds.PatientID

    # The destination bucket and filename on the MinIO server
    bucket_name = "annotstest"
    destination_file = f"{modality}/{patient_id}/{filename}"

    # Make the bucket if it doesn't exist.
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    # Upload the file, renaming it in the process
    client.fput_object(
        bucket_name, destination_file, source_file,
    )
    print(
        source_file, "successfully uploaded as object",
        destination_file, "to bucket", bucket_name,
    )
    final_annots_path = bucket_name + "/" + destination_file
    return final_annots_path,modality

def main():
    # Get the directory of the current script
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Construct the path to the dicom_files_download directory
    directory = os.path.join(root_dir, 'dicom_files_dowload')
    for filename in os.listdir(directory):
            if filename.endswith(".dcm"):
                local_image_url = os.path.join(directory, filename)
                path_fput, type = fput_minio(local_image_url,filename)

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)