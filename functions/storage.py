from google.cloud import storage
import json

# Initialization
creds = {
    "type": "service_account",
    "project_id": "tranquil-sunup-283012",
    "private_key_id": "f438d8b6739db03d8028cd085e29b4c53ff1b867",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC8DRokmIiTBhfG\nnpREGLLQCFBQH37dMlMg4BRZYihI1yKd3Tvq0DoawuA0b8KBFuVqFZgZl40pBWI+\neQPX8HhSzcEXpF3k9+hqaefIw+u/1mb5pHjtjKVSV7GsdUFM4TKotnIH35KKM54r\n9rdZr0obQ17X4TzHVHwrCe2yEMpAG77nu/B1UzTH4L+tXO8F5Z4qUN/ctyEbEepa\nHYfmn6qwWJ59pXG1cbVCAKJP7HzqJ9RAPuccAUMbvXjkkK9svBiaEYSGn/k5o55l\nWpqXfEF2Niv7vT2vFWWnCfWVWyMvGlR4n+0Zs7XAyMAavTKtILczU15lu+ht8yQz\nCXLngiFVAgMBAAECggEASAXqn96N3GWmgItm9OfSwIuWmwFdGQH3xa0dDhjinfdL\nylOb6bTDtFE0BtFRGRj4V9eacB7T0US/GndF6hQvOWOVk2UAEzyB1xPl0sZ7Cffn\na7C7IhxOi0mMAqXME1JjESwDY5GU8fqQF32APsi8pNF6R0t8eEma3u8ICz2UANYV\njr6Ut9lHSr40rYTm6TnJ0Kt9OvGY5RDFRWal9TGq6G5w2gvcqOGJElR77isMj22V\na8waqcNd8e5GsI9dL/Y+mjevJJtrBUbQ9Jl9QWlfefPn9+tUwjICXzkzcVHvywsN\nu2JLJ1+/Ez3EJPMg7ausGbo0IjUa28E2vA3qfSjmRwKBgQD/sRlGNISjF+GAJ6FV\nPMBlRp954CkON8KgGC6WozRRcTo5SUFvx7x3n3twckPl9nv876t3bDqmqNzI0jfe\nDj2I8VNSO0REaRENvyFng8z5qtaSbOle+qtZShaTVLSZZGAZx5bMILQ+m9Q3Cz0E\njx9YLJY0GdMP1XnobcIwzrPi+wKBgQC8RyGBWxrloAKZbJ3xV8QkgyLMBzmSVT22\nuN/7YJUD/fqw2xnwtxsK5WzXjqhFaooEg0j75hMyygageAfKFB+8PUc8m5FQ6I/u\na3Zj0Fbhus5tljLM6D94zTSMchIutHBpRBMKtizSJSKkIbAWChc9fOlhGgyfnX7v\nUPEh3gZb7wKBgQD4bl4cNFLbFAzps5exdcGJpUC17fJ1+f+EBXreqdvfdaAYoPCP\nZwXbRH1vF9aYzRBTBZsYAXRLEa7TAE1/1146fB90uljuDxeev6H5LbouqqqowmFN\nA0kRDEc7BwYiM8Cby6zc0LnQSx+6C5VRpK3Twh5+qMjFjalRB7OyMGPfmQKBgQCA\nX4uT1JehS5maHLoQTYRaVOOL870obmB2ztVBY9gW8bxVi/7C50ZUBpxQ2V8YfYz/\niLhhsL0UWzVrgovlGBWPVsTUqUnKvdctfC4r3mju3l1T0R5wIkbsyhXzUO/e0n72\n90h4fEBRRKq6+JFEZbr03M+PuqAy0MM0z56qNeVmFwKBgEnsX4epAg2JDl5svlvK\n3YuBbPy9qldDyW0DhG9kr2zjn3iRs/PYSp1U51gFPE3ssQPhF4folSLfVsSUbLVQ\nShVUiQNEKzZAl+Jc2aE+9Z8GhYDFWL7n/rKhXPRs5kBFArk9khMCBfvYW9d5vvqr\nJeSjvth76V1usCKpayZeAuN7\n-----END PRIVATE KEY-----\n",
    "client_email": "storage-manager@tranquil-sunup-283012.iam.gserviceaccount.com",
    "client_id": "116880534893651206526",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/storage-manager%40tranquil-sunup-283012.iam.gserviceaccount.com"
}
  creds_file_name = "data.json"
  creds_location = os.getcwd() + "/" + creds_file_name
  print(creds_location)
  with open(creds_location, 'w') as fp:
      json.dump(creds, fp)
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=creds_location

storage_client = storage.Client()


def upload_file(src_file_location, dst_file_name, bucket_name="outliers", is_public=True):
    bucket = storage_client.bucket(bucket_name)
     blob = bucket.blob(name_for_bucket)
     blob.upload_from_filename(name)
