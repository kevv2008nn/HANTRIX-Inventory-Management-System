import os
import pickle
import shutil

from app.face_ai.face_engine import extract_embedding


def register_face(student_id, image_path):

    embedding = extract_embedding(image_path)

    if embedding is None:
        return False

    os.makedirs(
        "app/face_ai/embeddings",
        exist_ok=True
    )

    os.makedirs(
        "app/face_ai/dataset",
        exist_ok=True
    )

    shutil.copy(
        image_path,
        f"app/face_ai/dataset/{student_id}.jpg"
    )

    with open(
        f"app/face_ai/embeddings/{student_id}.pkl",
        "wb"
    ) as f:

        pickle.dump(
            embedding,
            f
        )

    return True