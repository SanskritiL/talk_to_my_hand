import cv2
import numpy as np
from keras.models import load_model
from skimage.transform import resize, pyramid_reduce
import PIL
from PIL import Image
import os
import flask
import io
#from flask_cors import CORS, cross_origin



app = flask.Flask(__name__)
#CORS(app, support_credentials=True)
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
    
@app.route('/detect', methods=['POST'])
#@cross_origin(supports_credentials=True)
def detect():
    l = []
    data = {"success": False}
    if flask.request.method == "POST":
            print("SEEEEE ME\n\n\n\n\n")
            image = flask.request.files['image']
            print("SEEEEE ME 2\n\n\n\n\n")

            print(image)
            image.save('delete.png')
            image_frame = cv2.imread('delete.png')
#            image = Image.open(image)
#            image_frame = np.array(image)
#            npimg = np.fromstring(image, np.uint8)
#            image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
##            image = Image.open(io.BytesIO(image))
#            image_frame = cv2.imread(image)

#            to_pil = transforms.ToPILImage()
#            image = prepare_image(image)
#            output = model(image)
#            index = output.data.cpu().numpy().argmax()
#            data={}
#            data["predictions"] = "Looks like it is a " + str(index)
#            print(data)
#            data["success"] = True
    
    

#        cam_capture = cv2.VideoCapture(0)
#        _, image_frame = cam_capture.read()
#    image_frame = cv2.imread('t.png')
# Select ROI
#        im2 = crop_image(image_frame, 300,300,300,300)
    image_grayscale = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

    image_grayscale_blurred = cv2.GaussianBlur(image_grayscale, (15,15), 0)
    im3 = cv2.resize(image_grayscale_blurred, (28,28), interpolation = cv2.INTER_AREA)



    im4 = np.resize(im3, (28, 28, 1))
    im5 = np.expand_dims(im4, axis=0)


    pred_probab, pred_class = keras_predict(model, im5)

    curr = prediction(pred_class)
    print('SUP')
    print(curr)
#        cv2.putText(image_frame, curr, (700, 300), cv2.FONT_HERSHEY_COMPLEX, 4.0, (255, 255, 255), lineType=cv2.LINE_AA)
    return flask.jsonify(curr)

            
    
 
    # Display cropped image
#        cv2.rectangle(image_frame, (300, 300), (600, 600), (255, 255, 00), 3)
#        cv2.imshow("frame",image_frame)
#
#
#    #cv2.imshow("Image4",resized_img)
#        cv2.imshow("Image3",image_grayscale_blurred)
#
#        if cv2.waitKey(25) & 0xFF == ord('q'):
#                cv2.destroyAllWindows()
#                break


if __name__ == '__main__':
    model = load_model('CNNmodel.h5')
    model._make_predict_function()
    app.run(host='0.0.0.0', port=8002)

#cam_capture.release()
#cv2.destroyAllWindows()
