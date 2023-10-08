import os
from google.cloud import vision
from google.oauth2 import service_account
from PIL import Image
import base64


# Replace 'your-service-account-key.json' with the path to your JSON key file.
credentials = service_account.Credentials.from_service_account_file(
    'cygio-380509-f8e242fade84.json',
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

client = vision.ImageAnnotatorClient(credentials=credentials)
image = "images/jj.avif"


def readFile():
    # Read the image file and encode it to Base64
    with open(image, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    return image_data

image_data = readFile()

def is_base64(string):
    try:
        base64.b64decode(string, validate=True)
        return True
    except Exception as err:
        return False

if is_base64(image_data):
    image = vision.Image(content=image_data)
    # Perform landmark detection
    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations

    if landmarks:
        for landmark in landmarks:
            print(f"Landmark: {landmark.description}")
            print(f"Confidence: {landmark.score:.2f}")
    else:
        print("No landmarks detected.")
else:
    print("Invalid Base64 image data")



