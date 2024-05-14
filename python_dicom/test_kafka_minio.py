import json
from datetime import datetime
import random
import asyncio
from consumer import KafkaEventConsumer
from producer import KafkaEventProducer
import uuid
import os
import pydicom
from minio import Minio
from minio import Minio
from minio.error import S3Error
from DicomManager import DicomManager
import os
# from python_dicom import DicomManager, DicomUploader, DicomProcessor, DicomClientServer, DicomDownloader, DicomFileWriter
import requests
import multiprocessing
import time

base_url = 'http://localhost:8042'

username = 'orthanc'
password = 'orthanc'
auth = (username, password)

my_session = requests.session()

dicom_manager = DicomManager(my_session, base_url, auth)

# Get the directory of the current script
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Định nghĩa Consumer
consumer = KafkaEventConsumer(
    bootstrap_servers=["localhost:9092"],
    topics=["broncho_segment"],
    group="consumer_1"
)

# Định nghĩa Producer
producer = KafkaEventProducer(
    bootstrap_servers=["localhost:9092"],
    topic=["broncho_segment","broncho_segment_annots"]
)

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

def fget_minio(image_url):
    bucket_name, file_path = image_url.split('/', 1)

    # Name of the file you want to fetch
    file_name = os.path.basename(file_path)

    # Local file path where the fetched file will be saved
    local_file_path = os.path.join(root_dir, "minio_files", file_name)
    print(local_file_path)

    client.fget_object(bucket_name, file_path, local_file_path)
    print("File fetched successfully.")

    return local_file_path, file_name

# Xử lý event
async def handle_message1(message):
    offset = message.offset
    topic = message.topic
    partition = message.partition
    data = json.loads(message.value)
    print(offset, topic, partition, data)

    # Kéo ảnh từ minio về
    try:
        local_file_path, filename = fget_minio(data["image_url"])
    except S3Error as exc:
        print("error occurred.", exc)

    

# Xử lý event
async def handle_message(message):
    offset = message.offset
    topic = message.topic
    partition = message.partition
    data = json.loads(message.value)
    print(offset, topic, partition, data)

    # Kéo ảnh từ minio về
    try:
        local_file_path = fget_minio(data["image_url"])
    except S3Error as exc:
        print("error occurred.", exc)

    # Xử lý ảnh
    #annots_file_path = saveResult(local_file_path, filename)

    # Đẩy ảnh lên minio
    annots_file_path = f"annotstest/handled"
    try:
        annots_minio_path, modality = fput_minio(annots_file_path, filename)
    except S3Error as exc:
        print("error occurred.", exc)

    # Định nghĩa là data event để trả về
    data_final = {
        "task_id": data["task_id"], 
        "service_type": "abc",
        "annotation": annots_minio_path
    }

    # Gửi lại event lên kafka
    await producer.flush(data_final, "broncho_segment_annots")

    await consumer.commit(topic=topic, partition=partition, offset=offset)

def start_listening():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(dicom_manager.start_listening())
    loop.close()

async def main():
    # Start start_listening in a new process
    p = multiprocessing.Process(target=start_listening)
    p.start()

    # dicom_manager.get_all_studies()
    # Construct the path to the dicom_files_download directory
    directory = os.path.join(root_dir, 'dicom_files_import', 'new_file')
    # await producer.start()

    while True:
        for filename in os.listdir(directory):
            if filename.endswith(".dcm"):
                local_image_url = os.path.join(directory, filename)
                path_fput, type = fput_minio(local_image_url,filename)
                # Giả lập 1 event dummy
                data = {
                    "task_id": str(uuid.uuid4()), 
                    "image_type": type,
                    "image_url": path_fput,
                    "time": datetime.now().isoformat()
                }
                os.remove(local_image_url)  # Delete the file
                # await producer.flush(data, "broncho_segment")

    # Wait for a while before checking the directory again
        time.sleep(3)  # 10 seconds

    # consumer.handle = handle_message
    # await consumer.start()
    
    # await consumer.stop()
    # await producer.stop()

asyncio.run(main())