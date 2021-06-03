<!-- ABOUT THE PROJECT -->
## About The Cloud
Test

<!-- GETTING STARTED -->
## Getting Started

### Creating Cloud Storage Bucket
1. Open the Cloud Shell
2. Set environment variable for specify option
   ```sh
   PROJECT_ID=intelik-nutrient-detection
   STORAGE_CLASS=STANDARD
   BUCKET_LOCATION=ASIA-SOUTHEAST2
   BUCKET_NAME=intelik-nutrient-detection-bucket
   ```
3. Create the Bucket
   ```sh
   gsutil mb -p ${PROJECT_ID} -c ${STORAGE_CLASS} -l ${BUCKET_LOCATION} -b on gs://${BUCKET_NAME}
   ```

### Creating Cloud Datastore
1. From the GCP navigation menu, selecet **Databases > Datastore**
2. On **Get started** menu, **Select a Cloud Firestore mode** choose **Native Mode**
3. Then for the **Choose where to store your data** choose the location close to users and services. In here, choose `asia-southeast2 (Jakarta)`
4. Then **CREATE DATABASE**

