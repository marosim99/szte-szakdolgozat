import cv2
import pandas
import easyocr

pandas.set_option('display.max_rows', 100)
pandas.set_option('display.max_columns', 100)
pandas.set_option('display.width', 1000)

ID_CARD_PATH = "example_id_card.png"
reader = easyocr.Reader(['en'], gpu=False)


class CardLineItem:
    def __init__(self, top_left, top_right, btm_left, btm_right, text, conf):
        self.top_left = top_left
        self.top_right = top_right
        self.btm_left = btm_left
        self.btm_right = btm_right
        self.text = text
        self.conf = conf

    def __str__(self):
        return f"Text: {self.text}\ntop_left: {self.top_left}, top_right: {self.top_right}\n" \
               f"btm_left: {self.btm_left}, btm_right: {self.btm_right}, confidence: {self.conf}"


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


if __name__ == '__main__':
    data = reader.readtext(ID_CARD_PATH)
    # print(data[0])
    # data_frame = pandas.DataFrame(data, columns=['bbox', 'text', 'conf'])
    # print(data_frame)
    generate_image_with_bounding_boxes_on_words(data)

    card_line_items = list()

    for i in range(len(data)):
        item_bl = data[i][0][0]
        item_br = data[i][0][1]
        item_tr = data[i][0][2]
        item_tl = data[i][0][3]
        item_text = data[i][1]
        item_conf = data[i][2]

        line_item = CardLineItem(item_tl, item_tr, item_bl, item_br, item_text, item_conf)
        card_line_items.append(line_item)

    for cli in card_line_items:
        print(cli.__str__())
        print("/-------/")
