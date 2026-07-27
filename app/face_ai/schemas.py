from pydantic import BaseModel


class FaceRecognitionRequest(BaseModel):
    image_path: str


class FaceRegistrationRequest(BaseModel):
    student_id: str
    image_path: str