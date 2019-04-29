import sys
import time
import json
import cv2
from imutils.video import VideoStream
import imutils
import dlib
from core.eye_closed import eye_closed

def main():
    EYE_AR_THRESH = 0.15

    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    print("[INFO] starting video stream thread...")

    vs = VideoStream(src=0, resolution=(1280, 960)).start()
    fileStream = False

    time.sleep(1.0)

    prev_face = None
    prev_idx = 0
    PREV_MAX = 100

    while True:
        if fileStream and not vs.more():
            break

        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        try:
            # TODO: 가장 커다란 면적의 결과를 가져오도록 고쳐야 함
            rect = detector(gray, 0)[0]
        except IndexError:
            rect = None

        if rect:
            prev_idx = 0

        if not rect:
            if prev_face is not None and prev_idx < PREV_MAX:
                rect = prev_face
                prev_idx += 1

        if rect:  # face found
            prev_face = rect

            shape = get_shape(predictor, gray, rect)

            leftEAR = get_ear(shape, lStart, lEnd)
            rightEAR = get_ear(shape, rStart, rEnd)

            print(json.dumps({
                'closed': eye_closed(leftEAR, rightEAR, EYE_AR_THRESH)
            }))
            sys.stdout.flush()

    vs.stop()

if __name__ == '__main__':
    main()
