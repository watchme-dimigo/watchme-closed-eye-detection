import time
import cv2
from imutils.video import VideoStream
import imutils
import dlib
from core.eye_closed import *
from core.utils import *
from audio import Audio


def main():
    audio = Audio('./assets/beep.wav')

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(
        './assets/shape_predictor_68_face_landmarks.dat')

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    vs = VideoStream(src=0, resolution=(1280, 960)).start()
    fileStream = False

    cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Frame', 1000, 800)

    prev_face = None
    prev_idx = 0
    PREV_MAX = 100

    detect_iters = 0
    in_custom = False  # EAR 수집 진행 중인지 여부
    closed_iters = 0
    closed_ears = []

    while True:
        if fileStream and not vs.more():
            break

        frame = vs.read()
        frame = imutils.resize(frame, width=960)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        try:
            rects = detector(gray, 0)
            rects = sorted(
                rects,
                key=lambda rect: rect.width() * rect.height(),
                reverse=True)
            # 면적(인식된 범위)이 가장 커다란 사각형(얼굴)을 가져옴
            rect = rects[0]
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

            draw_dlib_rect(frame, rect)
            draw_contours(frame, left_eye_shape)
            draw_contours(frame, right_eye_shape)

            (frame_h, frame_w, _) = frame.shape
            frame = put_korean(
                frame, '얼굴이 인식되었습니다.', (frame_w / 2 - 100, 10), color='GREEN')

            ear = round((leftEAR + rightEAR) / 2.0, 3)
            frame = put_korean(
                frame, '현재 EAR: %s' %
                ear, (frame_w / 2 - 100, 52), fontSacle=30, color='WHITE')

            if not in_custom:
                detect_iters += 1
                if detect_iters > 50:  # 처음 얼굴 인식 후 일정 프레임 동안 안정적으로 인식됨
                    frame = put_korean(
                        frame, '눈을 감아 주세요.', (frame_w / 2 - 100, 90), fontSacle=30, color='RED')
                    audio.play()
                    in_custom = True
                elif detect_iters > 10:
                    frame = put_korean(
                        frame,
                        '잠시 뒤 삐 소리가 들리면 다시 소리가 날 때까지 눈을 감아 주세요.',
                        (180,
                         90),
                        fontSacle=20,
                        color='WHITE')

            if in_custom:
                closed_iters += 1
                if closed_iters > 100:
                    audio.play()
                    print(closed_ears)
                    ear_thresh = round(sum(closed_ears) / 100, 3)
                    print(ear_thresh)
                    frame = put_korean(
                        frame, '[측정 완료] 평균 EAR: %s' %
                        ear_thresh, (180, 90), fontSacle=30, color='GREEN')
                    save_ear_thresh(ear_thresh)
                    cv2.imshow("Frame", frame)  # 프레임 표시
                    key = cv2.waitKey(5000) & 0xFF
                    cv2.destroyAllWindows()
                    vs.stop()
                    exit(0)
                else:
                    frame = put_korean(
                        frame, '눈을 감아 주세요.', (frame_w / 2 - 100, 90), fontSacle=30, color='RED')
                    closed_ears.append(ear)

        else:  # 얼굴이 인식되지 않음
            detect_iters = 0  # 초기화

            (frame_h, frame_w, _) = frame.shape
            frame = put_korean(frame, '얼굴을 찾을 수 없습니다.',
                               (frame_w / 2 - 100, 10), color='RED')

        cv2.imshow("Frame", frame)  # 프레임 표시

        # q 키를 눌러 종료
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # cv2.destroyAllWindows()
    # vs.stop()


if __name__ == '__main__':
    main()
