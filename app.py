from flask import Flask, render_template, request
import cv2
import os
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    # Get the image from the camera
    camera = cv2.VideoCapture(0)
    ret, image = camera.read()

    # Save the image locally
    cv2.imwrite('scanned_document.jpg', image)
    # Open the image file
    image = Image.open("scanned_document.jpg")
    # Convert the image to black and white
    image = image.convert('L')

    # Save the black and white image
    image.save("scanned_document.jpg")
    camera.release()

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
