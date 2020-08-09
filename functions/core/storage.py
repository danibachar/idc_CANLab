from google.cloud import storage
import json, os

creds_file_name = "data.json"
creds_location = os.getcwd() + "/" + creds_file_name
print("grrr")
print(creds_location)
print("grrr")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=creds_location

storage.blob._MAX_MULTIPART_SIZE = 5 * 1024* 1024
storage_client = storage.Client()

def upload_file(src_file_location, dst_file_name, bucket_name="outliers", is_public=True, delete_local_file=True):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(dst_file_name)
        blob.chunk_size = 5 * 1024 * 1024
        blob.upload_from_filename(src_file_location)
        if is_public:
            blob.make_public()
        if delete_local_file:
            _del_file(src_file_location)
        return blob.public_url
    except Exception as e:
        print(e)
        if delete_local_file:
            _del_file(src_file_location)
        return ""

def _del_file(file_name):
    try:
        os.remove(file_name)
    except Exception as e:
        print(e)
        pass
