import cv2
import pytesseract
from pytesseract import Output
import pandas

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ID_CARD_PATH = "../test_images/example_id_card.png"
CONF_LEVEL = 70

def generate_image_with_bounding_boxes_on_words(ocr_result):
    img = cv2.imread(ID_CARD_PATH)

    for i in range(len(ocr_result['text'])):
        if float(ocr_result['conf'][i]) >= CONF_LEVEL:
            (x, y, w, h) = (ocr_result['left'][i],
                            ocr_result['top'][i],
                            ocr_result['width'][i],
                            ocr_result['height'][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 10)

    output_img_to_window(img)

def output_img_to_window(img):
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.imshow("output", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print("Running image to string function:\n")
    print(pytesseract.image_to_string(ID_CARD_PATH, lang="eng", config='-c preserve_interword_spaces=0'))
    print("----------------------------------")
    print("Running image to data function:\n")
    data = pytesseract.image_to_data(ID_CARD_PATH, lang="eng", output_type=Output.DICT)
    data_frame = pandas.DataFrame(data, columns=['top', 'left', 'width', 'height', 'conf', 'text'])
    print(data_frame)
    print("----------------------------------")
    print("Running image to boxes function:\n")
    print(pytesseract.image_to_boxes(ID_CARD_PATH, lang="eng"))
    generate_image_with_bounding_boxes_on_words(data)
