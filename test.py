import cv2
import os

path = r"C:\Users\kevvn\Documents\Lab Automation\SmartLabOS\backend\test_images\kevin.jpg"  # Replace with your actual path

print("Exists:", os.path.exists(path))

img = cv2.imread(path)

print("Image:", img)

if img is None:
    print("OpenCV could not read the image")
else:
    print("Image loaded successfully")
    print("Shape:", img.shape)