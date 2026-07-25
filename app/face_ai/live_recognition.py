import cv2
import os
import pickle
import numpy as np

from app.face_ai.face_engine import extract_embedding

EMBEDDINGS_FOLDER = "app/face_ai/embeddings"


def recognize_frame(frame):

    temp_path = "temp_frame.jpg"

    cv2.imwrite(temp_path, frame)

    embedding = extract_embedding(temp_path)

    os.remove(temp_path)

    if embedding is None:
        return None, None

    best_match = None
    best_score = -1

    for file in os.listdir(EMBEDDINGS_FOLDER):

        if not file.endswith(".pkl"):
            continue

        with open(os.path.join(EMBEDDINGS_FOLDER, file), "rb") as f:
            saved = pickle.load(f)

        score = np.dot(
            embedding,
            saved
        ) / (
            np.linalg.norm(embedding)
            * np.linalg.norm(saved)
        )

        score = float(np.clip(score, -1, 1))

        if score > best_score:
            best_score = score
            best_match = file.replace(".pkl", "")

    if best_score > 0.5:
        return best_match, best_score

    return None, None


cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    student, confidence = recognize_frame(frame)

    if student is not None:

        cv2.putText(
            frame,
            f"{student} ({confidence:.2f})",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

    cv2.imshow("SmartLabOS Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()