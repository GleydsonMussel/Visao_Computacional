import cv2

def save_coefficients(mtx, dist, new_mtx, path):
    """ Save the camera matrix and the distortion coefficients to given path/file. """
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_APPEND)
    cv_file.write("M", mtx)
    cv_file.write("D", dist)
    cv_file.write("NM", new_mtx)
    cv_file.release()