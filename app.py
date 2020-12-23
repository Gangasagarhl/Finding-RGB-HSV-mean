from flask import Flask, render_template, request, send_from_directory
import cv2
import numpy as np

COUNT = 0
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1 # Used for removing cache

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/home', methods=['POST'])
def home():
    global COUNT
    img = request.files['image'] #imge variable recieves posted image from index

    img.save('static/{}.jpg'.format(COUNT))    # saves the image in static folder
    img_arr = cv2.imread('static/{}.jpg'.format(COUNT)) # reading from static folder
    rgb = cv2.cvtColor(img_arr,cv2.COLOR_BGR2RGB) # changing color space from bgr to rgb
    hsv = cv2.cvtColor(img_arr,cv2.COLOR_BGR2HSV)

    color_values ={}

    color_values['rmean'] = np.mean(rgb[:,:,0])
    color_values['gmean'] = np.mean(rgb[:,:,1])
    color_values['bmean'] = np.mean(rgb[:,:,2])
    color_values['hmean'] = np.mean(hsv[:,:,0])
    color_values['smean'] = np.mean(hsv[:,:,1])
    color_values['vmean']= np.mean(hsv[:,:,2])

    
    

    COUNT += 1
    return render_template('prediction.html', data=color_values)


@app.route('/load_img')
def load_img():
    global COUNT
    return send_from_directory('static', "{}.jpg".format(COUNT-1))


if __name__ == '__main__':
    app.run(debug=True)