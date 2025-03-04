# Author: LUN
# Email: lun@tmy.red
# Time : DEC 2024
# File : Cloudflare_R2_dummy_image_converter.py
# version : 0.1

import os
import boto3
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime

# Cloudflare R2 config
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
R2_ENDPOINT_URL = os.getenv('R2_ENDPOINT_URL')

# Initiate Boto3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    endpoint_url=R2_ENDPOINT_URL
)

def list_objects_in_folder_since(folder, timestamp):
    """List all objects in a specified folder since a given timestamp"""
    objects = s3_client.list_objects_v2(Bucket=R2_BUCKET_NAME, Prefix=folder)
    filtered_objects = [
        obj['Key'] for obj in objects.get('Contents', []) 
        if obj['LastModified'].replace(tzinfo=None) > timestamp
    ]
    return filtered_objects

def download_image(key):
    """save Cloudflare R2 image into BytesIO(in RAM space) then return IO stream"""
    response = s3_client.get_object(Bucket=R2_BUCKET_NAME, Key=key)
    return Image.open(BytesIO(response['Body'].read())) # will not save any images into local drive.

def convert_to_webp(image):
    """Convert images to visually near-lossless WebP format"""
    output = BytesIO()
    image.save(output, format='WEBP', quality=75)
    output.seek(0)
    return output

def upload_image(image_data, key):
    """upload converted image to Cloudflare R2"""
    s3_client.put_object(Bucket=R2_BUCKET_NAME, Key=key, Body=image_data, ContentType='image/webp')
    print(f"Uploaded Successfully: {key}")

def main():
    # Specify path in your CF bucket and timestamp
    input_folder = input("Please enter the path to the images in CF bucket you want to process: ")
    output_folder = input("Please enter the destination folder path for the converted images: ") # could be the same as input_folder
    timestamp_str = input("Provide the starting timestamp in the following exactly format: YYYY-MM-DD HH:MM:SS: ") # try UTC-6 timestamp
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

    # List all images in the input folder since the specified timestamp
    image_keys = list_objects_in_folder_since(input_folder, timestamp)

    for key in image_keys:
        
        image = download_image(key)

        
        webp_image_data = convert_to_webp(image)

        # create new Key path
        new_key = key.replace(input_folder, output_folder).rsplit('.', 1)[0] + '.webp'

        
        upload_image(webp_image_data, new_key)

        print(f"Successfully Done!: {key} -> {new_key}")

if __name__ == "__main__":
    main()

