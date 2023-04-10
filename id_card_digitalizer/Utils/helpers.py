import cv2
from Model import CardTextItem as cti

def generate_image_with_bounding_boxes_on_words(ocr_result, image_path):
    img = cv2.imread(image_path)

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

        text_item = cti.CardTextItem(item_tl, item_tr, item_bl, item_br, item_text, item_conf)
        card_text_items.append(text_item)

    return card_text_items


def print_card_text_items(card_text_items):
    for cti in card_text_items:
        print(cti.__str__())
        print("/-------/\n")


def items_to_dict(card_text_items):
    result_dict = dict()

    for cti in card_text_items:
        if cti.is_key:
            result_dict[cti] = cti.assigned_to

    return result_dict


def print_dict(items_dict):
    for key, value in items_dict.items():
        print(f"Key: {key.text}, value: {value.text}")
