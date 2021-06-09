import flask
import werkzeug
import time
import tensorflow as tf
import os
import json
import googleapiclient.discovery
from google.api_core.client_options import ClientOptions

from google.cloud import firestore

# Setup environment credentials (you'll need to change these)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "access-firestore.json" # change for your GCP key
PROJECT = "intelik-nutrient-detection-app" # change for your GCP project
REGION = "us-central1" # change for your GCP region (where your model is hosted)

# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()

app = flask.Flask(__name__)

base_classes2 = ['beer',
 'broccoli',
 'cabbage',
 'egg',
 'hamburger',
 'pasta',
 'potato',
 'strawberry',
 'watermelon']

classes_and_models = {
    "model": {
        "classes": base_classes2,
        "model_name": "intelik_model" # change to be your model name
    }
}

def predict_json(project, region, model, instances, version=None):
    """Send json data to a deployed model for prediction.

    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to Tensors.
        version (str): version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the 
            model.
    """
    # Create the ML Engine service object
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)

    # Setup model path
    model_path = "projects/{}/models/{}".format(project, model)
    if version is not None:
        model_path += "/versions/{}".format(version)

    # Create ML engine resource endpoint and input data
    ml_resource = googleapiclient.discovery.build(
        "ml", "v1", cache_discovery=False, client_options=client_options).projects()
    instances_list = instances.numpy().tolist() # turn input into list (ML Engine wants JSON)
    
    input_data_json = {"signature_name": "serving_default",
                       "instances": instances_list} 

    request = ml_resource.predict(name=model_path, body=input_data_json)
    response = request.execute()
    
    # # ALT: Create model api
    # model_api = api_endpoint + model_path + ":predict"
    # headers = {"Authorization": "Bearer " + token}
    # response = requests.post(model_api, json=input_data_json, headers=headers)

    if "error" in response:
        raise RuntimeError(response["error"])

    return response["predictions"]

# Create a function to import an image and resize it to be able to be used with our model
def load_and_prep_image(filename, img_shape=150, rescale=False):
#def load_and_prep_image(filename, img_shape=224, rescale=False):
  """
  Reads in an image from filename, turns it into a tensor and reshapes into
  (224, 224, 3).
  """
  # Decode it into a tensor
#   img = tf.io.decode_image(filename) # no channels=3 means model will break for some PNG's (4 channels)
  img = tf.io.decode_image(filename, channels=3) # make sure there's 3 colour channels (for PNG's)
  # Resize the image
  img = tf.image.resize(img, [img_shape, img_shape])
  # Rescale the image (get all values between 0 and 1)
  if rescale:
      return img/255.
  else:
      return img

def update_logger(image, model_used, pred_class, pred_conf, correct=False, user_label=None):
    """
    Function for tracking feedback given in app, updates and reutrns 
    logger dictionary.
    """
    logger = {
        "image": image,
        "model_used": model_used,
        "pred_class": pred_class,
        "pred_conf": pred_conf,
        "correct": correct,
        "user_label": user_label
    }   
    return logger

def make_prediction(image, model, class_names):
    """
    Takes an image and uses model (a trained TensorFlow model) to make a
    prediction.

    Returns:
     image (preproccessed)
     pred_class (prediction class from class_names)
     pred_conf (model confidence)
    """
    image = load_and_prep_image(image)
    # Turn tensors into int16 (saves a lot of space, ML Engine has a limit of 1.5MB per request)
    image = tf.cast(tf.expand_dims(image, axis=0), tf.int16)
    # image = tf.expand_dims(image, axis=0)
    preds = predict_json(project=PROJECT,
                         region=REGION,
                         model=model,
                         instances=image)
    pred_class = class_names[tf.argmax(preds[0])]
    #pred_class = tf.argmax(preds[0])
    pred_conf = tf.reduce_max(preds[0])
    return image, pred_class, pred_conf

CLASSES = classes_and_models["model"]["classes"]
MODEL = classes_and_models["model"]["model_name"]

@app.route('/', methods = ['GET', 'POST'])
def home():
    return json.dumps(value = {})
@app.route('/predict', methods = ['GET', 'POST'])
def handle_request():
    files_ids = list(flask.request.files)
    print("\nNumber of Received Images : ", len(files_ids))
    image_num = 1
    for file_id in files_ids:
        #print("\nSaving Image ", str(image_num), "/", len(files_ids))
        imagefile = flask.request.files[file_id]

        #filename = werkzeug.utils.secure_filename(imagefile.filename)
        #print("Image Filename : " + imagefile.filename)

        #timestr = time.strftime("%Y%m%d-%H%M%S")
        
        #imagefile.save(timestr+'_'+filename)

        image, pred_class, pred_conf = make_prediction(imagefile.read(), model=MODEL, class_names=CLASSES)

        print("Prediction: " + pred_class)

        image_num = image_num + 1
    print("\n")

    doc_ref = db.collection(u'nutrients').document(f'{pred_class.capitalize()}')

    doc = doc_ref.get().to_dict()
    data = {}
    for key in doc:
        if not 'USRDA' in key:
            data[key] = doc[key]

    #Diabet_save = "Yes" if doc['Diabet_save'] == True else "No"
    
    #value = {
    #    "Food": pred_class.capitalize(),
    #    "Diabet_save": Diabet_save
    #}
    return data


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))