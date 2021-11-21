import os
import cv2
from flask import Flask, render_template, request
from keras.models import load_model



app = Flask(__name__)
model = load_model('model/first_try.h5')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image = request.files['file']
        #print(image.filename)
        image.save(os.path.join("static", image.filename))
        user_img = cv2.imread(('static/' + image.filename))
        user_img = cv2.resize(user_img, (150, 150))
        user_img = user_img/255.0
        user_img = user_img.reshape(1, 150, 150, 3)
        x = (model.predict(user_img) > 0.5).astype("int32")
        print(x)
        if(x[0][0]== 0):
            label = 'Your animal is Cat'
        else:
            label = 'Your animal is Dog'

        return render_template('index.html', label = label, img_path = 'static/' + image.filename)
        #return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True)
