# Google Cloud Platform Setup Script
# Requires `gcloud` setup and run with the Service Account key

export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS:-~/Keys/oppie/breef.json}

echo "Service account key location: $GOOGLE_APPLICATION_CREDENTIALS" 

# Connects to Service Account
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

# Enables All Services
gcloud services enable \
  cloudresourcemanager.googleapis.com \
  compute.googleapis.com \
  cloudbuild.googleapis.com \
  containerregistry.googleapis.com \
  iam.googleapis.com