from configparser import ConfigParser
import cv2

def load_ear_thresh(debug):
    try:
        config = ConfigParser()
        config.read('./settings.ini')
        ear_thresh = config['core'].getfloat('ear_thresh')
    except:
        print('[!] Failed to open file settings.ini; Using default value 0.18')
        ear_thresh = 0.18

    if debug:
        print('[*] EAR_THRESH:', ear_thresh)

    return ear_thresh

# frame draws: 실제 촬영된 영상 확인 시 테스트용으로 사용함; 실제 프로덕션 코드에는 없음

def _draw_rect(frame, rect):
    (x, y, w, h) = rect
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return rect


def draw_dlib_rect(frame, rect):
    # dlib.rectangle을 frame에 cv2 rectangle로 표시
    x, y = rect.left(), rect.top()
    return _draw_rect(frame, (x, y, rect.right() - x, rect.bottom() - y))


def draw_ndarray_rect(frame, rect):
    # x, y, w, h 형태의 numpy.ndarray을 frame에 cv2 rectangle로 표시
    return _draw_rect(frame, rect)


def draw_contours(frame, eye_shape):
    # eye_shape을 frame에 cv2의 contour로 표시
    eye_hull = cv2.convexHull(eye_shape)
    cv2.drawContours(frame, [eye_hull], -1, (0, 255, 0), 1)
