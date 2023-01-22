import cv2
import re
import pytesseract
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

ID_CARD_PATH = "example_id_card.png"
CONF_LEVEL = 80


class CardLineItem:
    def __init__(self, left, top, width, height, text):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.text = text

    def __str__(self):
        return f"Text: {self.text}\nLeft: {self.left}, Top: {self.top}\nWidth: {self.width}, Height: {self.height}"


def generate_image_with_bounding_boxes_on_letters(img_path):
    img = cv2.imread(img_path)
    h, w, c = img.shape

    boxes = pytesseract.image_to_boxes(img_path, lang="eng")

    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    # cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.imshow("output", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def generate_image_with_bounding_boxes_on_words(img_path):
    img = cv2.imread(img_path)
    img_dict = pytesseract.image_to_data(img_path, lang="eng", output_type=Output.DICT)

    for i in range(len(img_dict['text'])):
        if float(img_dict['conf'][i]) >= CONF_LEVEL:
            (x, y, w, h) = (img_dict['left'][i], img_dict['top'][i], img_dict['width'][i], img_dict['height'][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.imshow("output", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # generate_image_with_bounding_boxes_on_letters(id_card_path)
    generate_image_with_bounding_boxes_on_words(ID_CARD_PATH)
    # print(pytesseract.image_to_string("example_id_card.png", lang="eng"))
    # print(pytesseract.image_to_data("example_id_card.png", lang="eng"))
    # print(pytesseract.image_to_boxes("example_id_card.png", lang="eng"))

    ocr_result = pytesseract.image_to_data("example_id_card.png", lang="eng", output_type=Output.DICT)
    required_fields = ['left', 'top', 'width', 'height', 'conf', 'text']
    raw_card_data = {key: value for key, value in ocr_result.items() if key in required_fields}

    card_line_items = list()

    for i in range(len(raw_card_data.get('left'))):
        item_left = None
        item_top = None
        item_width = None
        item_height = None
        item_text = None
        item_conf = None

        for k, v in raw_card_data.items():
            if k == "left":
                item_left = v[i]
            elif k == "top":
                item_top = v[i]
            elif k == "width":
                item_width = v[i]
            elif k == "height":
                item_height = v[i]
            elif k == "conf":
                item_conf = v[i]
            elif k == "text":
                item_text = v[i]

        if item_conf >= CONF_LEVEL:
            line_item = CardLineItem(item_left, item_top, item_width, item_height, item_text)
            card_line_items.append(line_item)

    for cli in card_line_items:
        print(cli.__str__())
        print("/-------/")
