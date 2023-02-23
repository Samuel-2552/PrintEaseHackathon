from flask import Flask, render_template, request
import cv2
import os
from PIL import Image
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image_file = request.files['image']
        # Save the image file to disk
        image_file.save('image.jpg')
        return 'Image uploaded successfully'
    else:
        return 'No image uploaded'



if __name__ == '__main__':
    app.run(debug=True)
