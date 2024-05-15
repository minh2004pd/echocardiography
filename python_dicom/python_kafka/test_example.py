# Thêm function inference
# Ví dụ 
# def saveResult(local_file_path, filename)
# Trả về link url của ảnh annotation

import json
from datetime import datetime
import random
import asyncio
from consumer import KafkaEventConsumer
from producer import KafkaEventProducer
import uuid
import os
import pydicom

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


from minio import Minio
from minio import Minio
from minio.error import S3Error
import os

# Lấy dữ liệu từ datalake minio 
# Thay đổi key trong client
# def fput_minio(image_url, filename):
#     # Create a client with the MinIO server playground, its access key
#     # and secret key.
#     client = Minio("localhost:9010",
#         access_key="test123",
#         secret_key="19082004",
#         secure=False
#     )

#     # The file to upload, change this path if needed
#     source_file = image_url

#     # The destination bucket and filename on the MinIO server
#     bucket_name = "test"
#     destination_file = filename

#     # Make the bucket if it doesn't exist.
#     found = client.bucket_exists(bucket_name)
#     if not found:
#         client.make_bucket(bucket_name)
#         print("Created bucket", bucket_name)
#     else:
#         print("Bucket", bucket_name, "already exists")

#     # Upload the file, renaming it in the process
#     client.fput_object(
#         bucket_name, destination_file, source_file,
#     )
#     print(
#         source_file, "successfully uploaded as object",
#         destination_file, "to bucket", bucket_name,
#     )
#     final_annots_path = bucket_name + "/" + destination_file
#     return final_annots_path
def fput_minio(local_image_url, filename):
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio("localhost:9010",
        access_key="test123",
        secret_key="05112004pd",
        secure=False
    )

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
# Đẩy dữ liệu lên datalake minio 
# Thay đổi key trong client
# def fget_minio(image_url):
#     # Create a client with the MinIO server playground, its access key
#     # and secret key.
#     client = Minio("localhost:9010",
#         access_key="test123",
#         secret_key="19082004",
#         secure=False
#     )

#     directory, filename = os.path.split(image_url)

#     # Name of the bucket containing the file
#     bucket_name = directory

#     # Name of the file you want to fetch
#     file_name = filename

#     # Local file path where the fetched file will be saved
#     local_file_path = "/workspace/ailab/kc4.0utp-boilerplate/data_minio_test/" + file_name

#     client.fget_object(bucket_name, file_name, local_file_path)
#     print("File fetched successfully.")

#     return local_file_path, file_name
def fget_minio(image_url):
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio("localhost:9010",
        access_key="test123",
        secret_key="05112004pd",
        secure=False
    )

    directory, filename = image_url.split('/', 1)

    # Name of the bucket containing the file
    bucket_name = directory

    # Name of the file you want to fetch
    file_name = filename

    # Local file path where the fetched file will be saved
    local_file_path = "D:\OneDrive\\Máy tính\\python_dicom\\dicom_files_import\\new_file_dicom" + file_name
    print(local_file_path)

    client.fget_object(bucket_name, file_name, local_file_path)
    print("File fetched successfully.")

    return local_file_path, file_name
# Xử lý event
async def handle_message(message):
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

    # Xử lý ảnh
    #annots_file_path = saveResult(local_file_path, filename)

    # Đẩy ảnh lên minio
    annots_file_path = "annotstest/handled"
    try:
        annots_minio_path = fput_minio(annots_file_path, filename)
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

async def main():
    # Giả lập 1 event dummy
    await producer.start()
    local_image_url = "D:/kc4.0_boilerplate-main/kc4.0_boilerplate-main/0009.DCM"
    filename = "0009.DCM"
    path_fput,typee = fput_minio(local_image_url,filename)
    data = {
        "task_id": str(uuid.uuid4()), 
        "image_type": typee,
        "image_url": path_fput,
        "time": datetime.now().isoformat()
    }
    await producer.flush(data, "broncho_segment")

    consumer.handle = handle_message
    await consumer.start()
    
    await consumer.stop()
    await producer.stop()

asyncio.run(main())