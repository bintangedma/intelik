import os
import json
import re
import requests
import SessionState
import streamlit as st
import tensorflow as tf
from utils import load_and_prep_image, classes_and_models, update_logger, predict_json
from google.cloud import firestore

# Setup environment credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "access-firestore.json" # GCP key
PROJECT = "intelik-nutrient-detection-app" # GCP project
REGION = "us-central1" # GCP region 

# determined by the GOOGLE_APPLICATION_CREDENTIALS environment variable
db = firestore.Client()

#set page
st.set_page_config(page_title='NutriCheck', page_icon=None, layout='centered', initial_sidebar_state='auto')

st.title("NutriCheck")
st.header("Nutrient detection app, for self-management of diabetes foods")

@st.cache
def make_prediction(image, model, class_names):
    """
    Takes an image and uses model (a trained TensorFlow model) to make a
    prediction.

    Returns:
     image (preproccessed)
     pred_class (prediction class from class_names)
    """
    image = load_and_prep_image(image) # prep image

    image = tf.cast(tf.expand_dims(image, axis=0), tf.int16)

    # predict using deployed ml model
    preds = predict_json(project=PROJECT,
                         region=REGION,
                         model=model,
                         instances=image)

    pred_class = class_names[tf.argmax(preds[0])]

    return image, pred_class

CLASSES = classes_and_models["model"]["classes"]
MODEL = classes_and_models["model"]["model_name"]

# Display info about and classes
if st.checkbox("Show classes"):
    st.write(f"These are the classes of food it can identify:\n", CLASSES)

# File uploader allows user to add their own image
uploaded_file = st.file_uploader(label="Upload an image of food",
                                 type=["png", "jpeg", "jpg"])

# Setup session state to remember state of app so refresh isn't always needed
# See: https://discuss.streamlit.io/t/the-button-inside-a-button-seems-to-reset-the-whole-app-why/1051/11 
session_state = SessionState.get(pred_button=False)

# Create logic for app flow
if not uploaded_file:
    st.warning("Please upload an image.")
    st.stop()
else:
    session_state.uploaded_image = uploaded_file.read()
    st.image(session_state.uploaded_image, use_column_width=True)
    pred_button = st.button("Detect")

# Did the user press the predict button?
if pred_button:
    session_state.pred_button = True 

# And if they did...
if session_state.pred_button:
    session_state.image, session_state.pred_class = make_prediction(session_state.uploaded_image, model=MODEL, class_names=CLASSES)
    
    doc_ref = db.collection(u'nutrients').document(f'{session_state.pred_class.capitalize()}')

    doc = doc_ref.get().to_dict()
    Diabet_save = "Yes" if doc['Diabet_save'] == True else "No"

    st.header('RESULT')

    st.write(f"Food: {session_state.pred_class.capitalize()}")
    st.write(f'Diabetes save: {Diabet_save}')
    st.subheader('Nutrient content:')
    for key in doc:
        if not 'USRDA' in key and key != 'Food' and not 'Diabet' in key:
            items = re.split('_', key)
            st.write(f'{items[0]}: {str(doc[key])}{items[1]}')
    
# TODO: code could be cleaned up to work with a main() function...
# if __name__ == "__main__":
#     main()