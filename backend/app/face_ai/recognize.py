import os
import pickle

from app.face_ai.face_engine import extract_embedding


EMBEDDINGS_FOLDER = "app/face_ai/embeddings"

MATCH_THRESHOLD = 0.50


def recognize_face(image_path):
    import numpy as np

    embedding = extract_embedding(image_path)

    if embedding is None:
        return None

    if not os.path.exists(EMBEDDINGS_FOLDER):
        return None

    best_student_id = None
    best_score = -1.0

    for file in os.listdir(EMBEDDINGS_FOLDER):

        if not file.endswith(".pkl"):
            continue

        file_path = os.path.join(
            EMBEDDINGS_FOLDER,
            file
        )

        try:

            with open(file_path, "rb") as f:
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

                best_student_id = file.replace(
                    ".pkl",
                    ""
                )

        except Exception:
            continue

    if (
        best_student_id is not None
        and best_score >= MATCH_THRESHOLD
    ):

        return {
            "student_id": best_student_id,
            "confidence": float(best_score)
        }

    return None