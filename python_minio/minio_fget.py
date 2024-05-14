from minio import Minio

from minio import Minio
from minio.error import S3Error
import os

# Get the directory of the current script
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fget_minio(image_url):
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio("localhost:9010",
        access_key="minh2004pd",
        secret_key="05112004pd",
        secure=False
    )

    bucket_name, file_path = image_url.split('/', 1)

    # Name of the file you want to fetch
    file_name = os.path.basename(file_path)

    # Local file path where the fetched file will be saved
    local_file_path = os.path.join(root_dir, "minio_files", file_name)
    print(local_file_path)

    client.fget_object(bucket_name, file_path, local_file_path)
    print("File fetched successfully.")

    return local_file_path, file_name

if __name__ == "__main__":
    try:
        fget_minio("annotstest/MR/TCGA-CS-5396/10.dcm")
    except S3Error as exc:
        print("error occurred.", exc)