import sys
import json
from configparser import ConfigParser
import cv2
from imutils.video import VideoStream
import imutils
import dlib
from core.eye_closed import *
from core.utils import *


def main(debug=False):
    # 커스터마이제이션 설정이 있는 파일을 열어 ear_thresh 값(eye aspect ratio에 대한 임계값)을 가져옴
    config = ConfigParser()
    config.read('./settings.ini')
    ear_thresh = config['core'].getfloat('ear_thresh')
    
    if debug:
      print('[*] EAR_THRESH:', ear_thresh)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

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
        frame = imutils.resize(frame, width=960)
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
                rect = prev_face  # 결과가 없는 경우 적절히 오래된(PREV_MAX) 이전 결과를 사용
                prev_idx += 1

        if rect:  # 얼굴을 인식한 경우(prev_face를 사용하는 경우 포함)
            prev_face = rect  # 저장

            shape = get_shape(predictor, gray, rect)

            left_eye_shape = get_eye_shape(shape, lStart, lEnd)
            leftEAR = get_ear(left_eye_shape)

            right_eye_shape = get_eye_shape(shape, rStart, rEnd)
            rightEAR = get_ear(right_eye_shape)

            if debug:  # 디버그 모드에서 발견된 결과 표시
                draw_dlib_rect(frame, rect)
                draw_contours(frame, left_eye_shape)
                draw_contours(frame, right_eye_shape)

            print(json.dumps({
                'closed': eye_closed(leftEAR, rightEAR, ear_thresh, debug)
            }))

        else:
            print(json.dumps({
                'closed': -1
            }))

        sys.stdout.flush()

        if debug:  # 디버그 모드
            cv2.imshow("Frame", frame)  # 프레임 표시

            # q 키를 눌러 종료
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    cv2.destroyAllWindows()
    vs.stop()


if __name__ == '__main__':
    # NOTE: turn debug mode off (default) in production or test for C# parent
    # main()
    main(debug=True)
