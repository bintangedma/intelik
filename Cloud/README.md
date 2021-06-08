<!-- ABOUT THE PROJECT -->
## About The Cloud
Test

<!-- GETTING STARTED -->
## Getting Started

### Creating Cloud Storage Bucket
1. Open the Cloud Shell
2. Set environment variable for specify option
   ```sh
   PROJECT_ID=intelik-nutrient-detection-app            # Set Project ID
   STORAGE_CLASS=STANDARD                           # Set Storage Class
   BUCKET_LOCATION=ASIA-SOUTHEAST2                  # Set Bucket Location
   BUCKET_NAME=intelik-nutrient-detection-app-bucket    # Set Bucket Name
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

<!--
5. After that, go to [Firebase console](https://console.firebase.google.com/), click **Create a project**.
6. For **Project name**, input/choose **INTELIK - Nutrient Detection**, accept for the **I accept the Firebase Terms**, then **Continue**
7. For **Confirm Firebase billing plan**, click **Confirm plan**. _Billing is shared between Firebase and Google Cloud_.
8. **Continue**
9. **Enable Google Analytics for this project** is optional. _on is recommended._
10. for **Analytics location** choose Indonesia, **Use the default settings**, also **I accept the Google Analytics terms** then **Add Firebase**
11. After the project already created, **Continue** to go to project overview.
-->

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