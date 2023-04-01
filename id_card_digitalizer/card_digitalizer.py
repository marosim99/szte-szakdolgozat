import cv2
import pandas
import easyocr
import helpers

pandas.set_option('display.max_rows', 100)
pandas.set_option('display.max_columns', 100)
pandas.set_option('display.width', 1000)

ID_CARD_PATH = "example_id_card.png"
reader = easyocr.Reader(['en'], gpu=False)


class CardTextItem:
    def __init__(self, top_left, top_right, btm_left, btm_right, text, conf):
        self.top_left = top_left
        self.top_right = top_right
        self.btm_left = btm_left
        self.btm_right = btm_right
        self.text = text
        self.conf = conf
        self.is_examined = 0
        self.assigned_to = 0
        self.is_key = 0
        self.is_value = 0

    def __str__(self):
        return f"Text: {self.text}\ntop_left: {self.top_left}, top_right: {self.top_right}\n" \
               f"btm_left: {self.btm_left}, btm_right: {self.btm_right}\n" \
               f"examined: {self.is_examined}, assigned: {0 if self.assigned_to == 0 else 1}"


def generate_image_with_bounding_boxes_on_words(ocr_result):
    img = cv2.imread(ID_CARD_PATH)

    for text in ocr_result:
        top_left = tuple(text[0][0])  # top left
        bottom_right = tuple(text[0][2])  # bottom right
        img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 10)

    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.imshow("output", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_text_items_from_ocr_data(ocr_data):
    card_text_items = list()

    for i in range(len(ocr_data)):
        item_bl = ocr_data[i][0][0]
        item_br = ocr_data[i][0][1]
        item_tr = ocr_data[i][0][2]
        item_tl = ocr_data[i][0][3]
        item_text = ocr_data[i][1]
        item_conf = ocr_data[i][2]

        text_item = CardTextItem(item_tl, item_tr, item_bl, item_br, item_text, item_conf)
        card_text_items.append(text_item)

    return card_text_items


def print_card_text_items(card_text_items):
    for cti in card_text_items:
        print(cti.__str__())
        print("/-------/")


if __name__ == '__main__':
    data = reader.readtext(ID_CARD_PATH)
    # print(data[0])
    # data_frame = pandas.DataFrame(data, columns=['bbox', 'text', 'conf'])
    # print(data_frame)
    # generate_image_with_bounding_boxes_on_words(data)
    items = get_text_items_from_ocr_data(data)
    print_card_text_items(items)
    print("-------------")

    # 1.
    min_y_item = helpers.find_min_y(items)
    # 2.
    max_y = helpers.find_max_y(items)
    # 3.
    min_x = helpers.find_min_x(items)
    # 4.
    max_x = helpers.find_max_x(items)

    print(max_y)
    print(min_x)
    print(max_x)

    helpers.find_pair(items[3], items)
    print_card_text_items(items)
    # print(items[3].assigned_to)
    # print(items[3].assigned_to.assigned_to)

