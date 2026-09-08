_face_app = None


def _get_face_app():
    global _face_app

    if _face_app is None:
        import cv2  # noqa: F401
        from insightface.app import FaceAnalysis

        _face_app = FaceAnalysis(name="buffalo_l")
        _face_app.prepare(ctx_id=-1, det_size=(640, 640))

    return _face_app

def extract_embedding(image_path):
    import cv2

    image = cv2.imread(image_path)
    if image is None:
        return None

    faces = _get_face_app().get(image)

    if len(faces)==0:
        return None

    return faces[0].embedding