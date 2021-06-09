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

### Deploying ML to Cloud AI Platform
1. Upload  and unzip [intelik-model-classes.zip](../ML/intelik-model-classes.zip) to the bucket that have been created before
2. From GCP go to **AI Platform > Models**
3. Create **NEW MODEL**, pesonalize the option
4. After model created, click the model then click **NEW VERSION**
5. Insert the name (ex. v001), choose **Pre-built Container**
   Python version **3.7**
   Framework **TensorFlow**
   Framework version **2.3.1**
   ML runtime version **2.3**
6. Click **Browe** and choose the ML model folder that you upload before (intelik-model-classes)
7. Leave other default, then **SAVE**