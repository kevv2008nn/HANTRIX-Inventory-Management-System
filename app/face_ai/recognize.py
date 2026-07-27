import os
import pickle
import numpy as np

from app.face_ai.face_engine import extract_embedding


def recognize_face(image_path):

    embedding = extract_embedding(image_path)

    if embedding is None:
        return None

    best_match = None
    best_score = -1

    folder = "app/face_ai/embeddings"

    for file in os.listdir(folder):

        if not file.endswith(".pkl"):
            continue

        with open(os.path.join(folder, file), "rb") as f:
            saved_embedding = pickle.load(f)

        score = np.dot(
            embedding,
            saved_embedding
        ) / (
            np.linalg.norm(embedding)
            * np.linalg.norm(saved_embedding)
        )

        if score > best_score:
            best_score = score
            best_match = file.replace(".pkl", "")

    if best_score > 0.5:
        return {
            "student_id": best_match,
            "confidence": float(best_score)
        }

    return None