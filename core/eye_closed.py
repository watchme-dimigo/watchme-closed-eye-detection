from scipy.spatial import distance as dist
from imutils import face_utils

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear

def get_shape(predictor, gray, rect):
    shape = predictor(gray, rect)
    return face_utils.shape_to_np(shape)

def get_eye_shape(shape, start, end):
    return shape[start:end]

def get_ear(eye_shape):
    return eye_aspect_ratio(eye_shape)

def eye_closed(left, right, thresh):
    ear = (left + right) / 2.0
    return int(ear < thresh)
