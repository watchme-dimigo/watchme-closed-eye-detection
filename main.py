import sys
import time
import json
import cv2
from imutils.video import VideoStream
import imutils
import dlib
from core.eye_closed import *
from core.utils import *

def main(debug=False):
    EYE_AR_THRESH = 0.15

    # print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # print("[INFO] starting video stream thread...")

    vs = VideoStream(src=0, resolution=(1280, 960)).start()
    fileStream = False

    if debug:
        cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Frame', 1000, 800)

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

            left_eye_shape = get_eye_shape(shape, lStart, lEnd)
            leftEAR = get_ear(left_eye_shape)

            right_eye_shape = get_eye_shape(shape, rStart, rEnd)
            rightEAR = get_ear(right_eye_shape)

            if debug:
                draw_dlib_rect(frame, rect)
                draw_contours(frame, left_eye_shape)
                draw_contours(frame, right_eye_shape)


            print(json.dumps({
                'closed': eye_closed(leftEAR, rightEAR, EYE_AR_THRESH)
            }))

        else:
            print(json.dumps({
                'closed': -1
            }))
            
        sys.stdout.flush()
        if debug:
            cv2.imshow("Frame", frame)  
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break    

    cv2.destroyAllWindows()
    vs.stop()

if __name__ == '__main__':
    # turn debug mode off (default) in production or test for C# parent
    # main()  
    main(debug=True)
