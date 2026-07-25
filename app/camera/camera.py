import cv2

from app.face_ai.recognizer import recognize

camera = cv2.VideoCapture(0)

print("Starting SmartLab AI Camera...")

last_student = None

while True:

    ret, frame = camera.read()

    if not ret:
        break

    cv2.imshow("SmartLab AI", frame)

    key = cv2.waitKey(1)

    if key == ord("c"):

        cv2.imwrite("current.jpg", frame)

        student = recognize("current.jpg")

        if student:

            if student != last_student:

                print("Recognized:", student)

                last_student = student

        else:

            print("Unknown Face")

    if key == 27:
        break

camera.release()

cv2.destroyAllWindows()