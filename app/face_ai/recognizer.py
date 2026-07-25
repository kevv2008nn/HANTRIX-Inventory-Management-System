import os
import pickle
import numpy as np

from app.face_ai.face_engine import extract_embedding

EMBEDDING_FOLDER = "app/face_ai/embeddings"


def cosine_similarity(a, b):

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def recognize(image_path):

    embedding = extract_embedding(image_path)

    if embedding is None:
        return None

    best_score = 0
    best_student = None

    for file in os.listdir(EMBEDDING_FOLDER):

        if not file.endswith(".pkl"):
            continue

        student_id = file.replace(".pkl", "")

        with open(
            os.path.join(EMBEDDING_FOLDER, file),
            "rb"
        ) as f:

            saved_embedding = pickle.load(f)

        score = cosine_similarity(
            embedding,
            saved_embedding
        )

        if score > best_score:
            best_score = score
            best_student = student_id

    if best_score < 0.55:
        return None

    return best_student