from configparser import ConfigParser
import cv2

def load_ear_thresh(debug):
    config = ConfigParser()
    config.read('./config.ini')

    try:
        ear_thresh = config['core'].getfloat('ear_thresh')
    except:
        ear_thresh = 0.18
        print('[!] Failed to open file config.ini; Using default value', ear_thresh)

        config.add_section('core')
        config.set('core', 'ear_thresh', str(ear_thresh))

        with open('./config.ini', 'w') as config_file:
            config.write(config_file)

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
