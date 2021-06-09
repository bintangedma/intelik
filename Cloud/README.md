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

### Create Service Account Key
1. From GCP, go to **IAM & Admin > Service Accounts** then **CREATE SERVICE ACCOUT**
2. Enter service account name then **CREATE AND CONTINUE**
3. For **Grant this service account access to project**, we will use the key for **accesing AI Platform Model** and **Read data from Firebase**
4. Skip the 3rd step, click **DONE**
5. After Service Account created, click the Service Account name then go to tab **KEY**
6. Click **ADD KEY** then **Create new key**
7. For key type choose **JSON**, click **CREATE**
8. Key will be downloaded, save it for auth later

### Deploy Web Service to Cloud App Engine
For web service, use Streamlite (python based) for the server. This web will provide user to predict food image using the deployed ML model on AI Platform, get the information from the Cloud Firestore and output the information including the food name, nutrient facts and diabet save status.
1. Upload [intelik-app-webservice](intelik-app-webservice) to cloud env
2. Open [app.py](intelik-app-webservice/app.py) and customize this line
```sh
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "access-firestore.json" # change with the service account key 
PROJECT = "intelik-nutrient-detection-app" # GCP project ID
REGION = "us-central1" # GCP region 
```
3. Open [utils.py](intelik-app-webservice/utils.py) and change the `model_name` with you deployed ML model name
```sh
classes_and_models = {
    "model": {
        "classes": base_classes,
        "model_name": "intelik_model" #Change this to you ML model name
    }
}
```
4. For deploying, in the folder already created [Makefile](intelik-app-webservice/Makefile) for the command
```sh
make gcloud-deploy
```

### Deploy Backservice to Cloud Run
For android backservice, using Flask (python based) for the server. service provide API for predict image. App only do the http request with image included to the '/predict' end-point. The server will predict the food image using the deployed ML model on AI Platform, get the information from the Cloud Firestore and return the information back to the app as JSON data.
1. Upload [intelik-app-backservice](intelik-app-backservice) to cloud env
2. Open [mail.py](intelik-app-backservice/mail.py) and customize this line
```sh
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "access-firestore.json" # change with the service account key 
PROJECT = "intelik-nutrient-detection-app" # GCP project ID
REGION = "us-central1" # GCP region 
```
also change `model_name` with you deployed ML model name
```sh
classes_and_models = {
    "model": {
        "classes": base_classes,
        "model_name": "intelik_model" #Change this to you ML model name
    }
}
```
3. Before deploy, build your container image using Cloud Build, by running the following command from the directory containing the Dockerfile:
```sh
gcloud builds submit --tag gcr.io/PROJECT-ID/name-of-the-app
```
4. For deploying, type this on Cloud Shell
```sh
gcloud run deploy --image gcr.io/PROJECT-ID/name-of-the-app
```
   If prompted to enable the API, Reply **y** to enable.
   You will be prompted for the service name: press Enter to accept the default name, `name-of-the-app`
   You will be prompted for region: select the region of your choice, for example `us-central1`
   You will be prompted to **allow unauthenticated invocations**: respond **y**