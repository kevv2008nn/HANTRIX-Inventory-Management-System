import cv2
import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis(
    name="buffalo_l"
)

app.prepare(
    ctx_id=-1,
    det_size=(640,640)
)

def extract_embedding(image_path):

    image = cv2.imread(image_path)

    faces = app.get(image)

    if len(faces)==0:
        return None

    return faces[0].embedding