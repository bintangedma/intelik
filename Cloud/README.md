<!-- ABOUT THE PROJECT -->
## About The Cloud
Test

<!-- GETTING STARTED -->
## Getting Started

### Creating Cloud Storage Bucket
1. Open the Cloud Shell
2. Set environment variable for specify option
   ```sh
   PROJECT_ID=intelik-nutrient-detection-app             # Set Project ID
   STORAGE_CLASS=STANDARD                                # Set Storage Class
   BUCKET_LOCATION=ASIA-SOUTHEAST2                       # Set Bucket Location
   BUCKET_NAME=intelik-nutrient-detection-app-bucket     # Set Bucket Name
   ```
3. Create the Bucket
   ```sh
   gsutil mb -p ${PROJECT_ID} -c ${STORAGE_CLASS} -l ${BUCKET_LOCATION} -b on gs://${BUCKET_NAME}
   ```

### Creating Cloud Datastore (Firestore)
1. From the GCP navigation menu, selecet **Databases > Firestore**
2. On **Get started** menu, **Select a Cloud Firestore mode** choose **Native Mode**
3. Then for the **Choose where to store your data** choose the location close to users and services. In here, choose `asia-southeast2 (Jakarta)`
4. Then **CREATE DATABASE**

### Importing Data to Firestore
1. Open cloud shell
2. Create new directory
   ```sh
   mkdir nutrients
   cd nutrients
   ```
3. Initialize npm
   ```sh
   npm init
   ```
   for the option, set like this
   ```sh
   {  
   "name": "nutrientsimport",  
   "version": "1.0.0",  
   "description": "Export Nutrients Data from .csv, then import it to Firestore",  
   "main": "index.js",  
   "scripts": {    "test": "echo \"Error: no test specified\" && exit 1"  },  
   "author": "ramadhan",  
   "license": "ISC"
   }
   ```
4. Installing dependencies
   ```sh
   npm install @google-cloud/firestore
   npm install csv-parse
   ```
5. Now, creating the execution code
   ```sh
   npm install @google-cloud/firestore
   npm install csv-parse
   ```
6. Create the scrip
   ```sh
   touch nutrientsDataImport.js
   ```
   You cas see the full script here: [nutrientsDataImport.js](nutrientsDataImport.js)
7. Upload the [nutrients.csv](nutrients.csv) to cloud, then run the script
   ```sh
   node nutrientsDataImport.js nutrients.csv
   ```