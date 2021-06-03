<!-- ABOUT THE PROJECT -->
## About The Cloud

<!-- GETTING STARTED -->
## Getting Started

### Creating Cloud Storage Bucket
1. Open the Cloud Shell
2. Prep for specify option
   ```sh
   export PROJECT_ID=intelik-nutrient-detection
   export STORAGE_CLASS=STANDARD
   export BUCKET_LOCATION=ASIA-SOUTHEAST2
   export BUCKET_NAME=intelik-nutrient-detection-bucket
   ```
3. Create the Bucket
   ```sh
   gsutil mb -p PROJECT_ID -c STORAGE_CLASS -l BUCKET_LOCATION -b on gs://BUCKET_NAME
   ```