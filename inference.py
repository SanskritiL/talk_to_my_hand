import cv2
import numpy as np
from keras.models import load_model
from skimage.transform import resize, pyramid_reduce
import PIL
from PIL import Image
import os
import flask
import io
from gtts import gTTS
from googletrans import Translator
import houndify
import sys
import base64

app = flask.Flask(__name__)
os.environ['KMP_DUPLICATE_LIB_OK']='True'


def prediction(pred):
    return(chr(pred+ 65))


def keras_predict(model, image):
    data = np.asarray( image, dtype="int32" )
    
    pred_probab = model.predict(data)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class

def keras_process_image(img):
    
    image_x = 28
    image_y = 28
    img = cv2.resize(img, (1,28,28), interpolation = cv2.INTER_AREA)
  
    return img
 

def crop_image(image, x, y, width, height):
    return image[y:y + height, x:x + width]

@app.route('/english_voice', methods=['POST'])
def english_voice():
    text = flask.request.get_json(force=True).get('text')
    # curl --header "Content-Type: application/json" --request POST --data '{"text":"hello"}' http://localhost:8001/english_voice

    requestInfo = {
      'Latitude': 37.388309,
      'Longitude': -121.973968,
      'ResponseAudioVoice': "Judy",
      'ResponseAudioShortOrLong': "Long",
      "OutputLanguageEnglishName":"Spanish",
      # 'ResponseAudioAcceptedEncodings': ["Speex"],
      "ClientMatches" : [{
        "Expression" : text,
        "Result" : {
        "Intent" : "speak_this"
        },
        "SpokenResponse" : text,
        "SpokenResponseLong" : text,
        "WrittenResponse" : " Hello! This is the text I am going to speak.",
        "WrittenResponseLong" : " Hello! This is the text I am going to speak."
    }]
    }

    client = houndify.TextHoundClient(CLIENT_ID, CLIENT_KEY, "test_user", requestInfo)


    response = client.query(text)

    base64_message = response['AllResults'][0]['ResponseAudioBytes']
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    with open('myfile.wav', mode='wb') as f:
      f.write(message_bytes)

    os.system('open myfile.wav')
   

    return flask.jsonify(text)

@app.route('/spanish_voice', methods=['POST'])
def spanish_voice():
    text = flask.request.get_json(force=True).get('text')

    translation = translator.translate(text, dest='es')
    spanish_text = translation.text
    tts = gTTS(text=spanish_text,lang='es')
    tts.save('spanish_text.mp3')
    os.system('open spanish_text.mp3')
    return flask.jsonify(text)

@app.route('/detect', methods=['POST'])
def detect():
    l = []

    # image = flask.request.files["image"]
    image = flask.request.get_json(force=True).get('image')

    dir = "images_treehacks/"
    filename = dir+image
    image_frame = cv2.imread(filename)

    image_grayscale = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

    image_grayscale_blurred = cv2.GaussianBlur(image_grayscale, (15,15), 0)
    im3 = cv2.resize(image_grayscale_blurred, (28,28), interpolation = cv2.INTER_AREA)



    im4 = np.resize(im3, (28, 28, 1))
    im5 = np.expand_dims(im4, axis=0)


    pred_probab, pred_class = keras_predict(model, im5)

    curr = prediction(pred_class)
    print(curr)
    return flask.jsonify(curr)




if __name__ == '__main__':
    model = load_model('CNNmodel.h5')
    model._make_predict_function()
    translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.es',
    ])


    CLIENT_ID = "v1EcICJJvSHSoO1MHa0kaQ=="
    CLIENT_KEY = "b6oThqYfe20yD_Hd1TRxiNNojyioPjz6m18ohsgzFVD7kN_yniOfVvGYPY_tch3xPYiypBBiO7zFPZTGdJsviw=="


    app.run(host='0.0.0.0', port=8001)

