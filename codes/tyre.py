import cv2
import numpy as np
from keras.models import load_model

# Load the trained model
model = load_model('tyre_classifier.h5')

# Load the video
cap = cv2.VideoCapture('video.mp4')

# Loop through each frame of the video
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame for input to the model
    resized = cv2.resize(frame, (128, 128))
    normalized = resized / 255.0
    reshaped = np.reshape(normalized, (1, 128, 128, 3))

    # Use the model to predict whether the frame contains a tyre or not
   
    prediction = model.predict(reshaped)[0][0]

    # If the model predicts that the frame contains a tyre, draw a rectangle around the detected object
    if prediction > 0.5:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Tyre Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()