from google.cloud import storage

def download_blob(bucket_name, source_blob_name, destination_file_name):
  """Downloads a blob from a Google Cloud Storage bucket."""
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucket_name)
  blob = bucket.blob(source_blob_name)

  blob.download_to_filename(destination_file_name)

  print('Blob {} downloaded to {}.'.format(
      source_blob_name,
      destination_file_name))

def percentage_difference(first_str, second_str):
  """Calculates the difference in string length as a fractional representation of a percentage."""
  return (1 - float(len(first_str)) / len(second_str))