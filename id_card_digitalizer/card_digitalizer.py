import cv2
import pandas
import easyocr
import helpers
import CardTextItem
import card_digitalizer_tests

pandas.set_option('display.max_rows', 100)
pandas.set_option('display.max_columns', 100)
pandas.set_option('display.width', 1000)

ID_CARD_PATH = "example_id_card.png"
reader = easyocr.Reader(['en'], gpu=False)


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

        text_item = CardTextItem.CardTextItem(item_tl, item_tr, item_bl, item_br, item_text, item_conf)
        card_text_items.append(text_item)

    return card_text_items

if __name__ == '__main__':
    data = reader.readtext(ID_CARD_PATH)
    # print(data[0])
    # data_frame = pandas.DataFrame(data, columns=['bbox', 'text', 'conf'])
    # print(data_frame)
    # generate_image_with_bounding_boxes_on_words(data)
    items = get_text_items_from_ocr_data(data)
    # helpers.print_card_text_items(items)
    print("/-- OCR process finished --/")

    helpers.find_key_value_pairs(items)
    helpers.print_card_text_items(items)


