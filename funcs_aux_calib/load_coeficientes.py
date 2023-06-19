import cv2

def load_coefficients(path):
    """ Loads camera matrix and distortion coefficients. """
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
    camera_matrix = cv_file.getNode("M").mat()
    dist_matrix = cv_file.getNode("D").mat()
    new_camera_matrix = cv_file.getNode("NM").mat
    cv_file.release()
    return [camera_matrix, dist_matrix, new_camera_matrix]
    