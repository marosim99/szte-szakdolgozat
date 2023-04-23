import cv2


def preprocess_image(img):
    grayscale_img = convert_to_grayscale_image(img)
    de_noised_img = remove_noise(grayscale_img)
    threshold_img = threshold_image(de_noised_img)

    return threshold_img


def convert_to_grayscale_image(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def remove_noise(image):
    return cv2.medianBlur(image, 5)


def threshold_image(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)[1]


def show_image(img):
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.imshow("output", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def read_image(path):
    return cv2.imread(path)


