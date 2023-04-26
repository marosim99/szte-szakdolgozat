import os
import re
import csv
import cv2
import pathlib
from Models import CardTextItem as cti

YYYY_MM_DD_REGEX = "(?:19/d{2}|20[0-9][0-9])[-/.](?:0[1-9]|1[012])[-/.](?:0[1-9]|[12][0-9]|3[01])"
DD_MM_YYYY_REGEX = "(?:0[1-9]|[12][0-9]|3[01])[-/.](?:0[1-9]|1[012])[-/.](?:19/d{2}|20[0-9][0-9])"
MM_DD_YYYY_REGEX = "(?:0[1-9]|1[012])[-/.](?:0[1-9]|[12][0-9]|3[01])[-/.](?:19/d{2}|20[0-9][0-9])"
COUNTRY_CODE_REGEX = "^[a-zA-Z]{2,3}$"
DOCUMENT_NUMBER_REGEX = "^(.*\d){4,}\S*$"
FILE_EXT = "csv"


def draw_bounding_boxes_around_on_words(ocr_result, image):
    for text in ocr_result:
        top_left = tuple(text[0][0])
        bottom_right = tuple(text[0][2])
        cv2.rectangle(image, top_left, bottom_right, (50, 170, 90), 10)


def draw_bounding_boxes_around_key_value_pairs(card_text_items, image):
    for item in card_text_items:
        if item.is_key:
            bottom_left = tuple(item.btm_left)
            top_right = tuple(item.assigned_to.top_right)
            cv2.rectangle(image, bottom_left, top_right, (170, 50, 130), 14)

    cv2.namedWindow("output", cv2.WINDOW_KEEPRATIO)
    cv2.imshow("output", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_bounding_boxes(ocr_result, card_text_items, image):
    draw_bounding_boxes_around_on_words(ocr_result, image)
    draw_bounding_boxes_around_key_value_pairs(card_text_items, image)


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
    for item in card_text_items:
        print(item)
        print("/-------/\n")


def items_to_dict(card_text_items):
    result_dict = dict()

    for cti in card_text_items:
        if cti.is_key:
            result_dict[cti.text] = cti.assigned_to.text
        elif not cti.is_key and not cti.is_value and cti.assigned_to == 0:
            result_dict[cti.text] = "N/A"

    return result_dict


def print_dict(items_dict):
    for key, value in items_dict.items():
        print(f"Key: {key}, Value: {value}")


def post_process_text(items_dict):
    new_items_dict = dict()

    for key, value in items_dict.items():
        cleaned_string = value.replace(' ', '')
        if matches_any_regex(cleaned_string):
            new_items_dict[key.replace(':', '')] = cleaned_string
        else:
            new_items_dict[key.replace(':', '')] = value

    return new_items_dict


def matches_any_regex(text):
    if re.search(YYYY_MM_DD_REGEX, text):
        return True
    if re.search(DD_MM_YYYY_REGEX, text):
        return True
    if re.search(MM_DD_YYYY_REGEX, text):
        return True
    if re.search(COUNTRY_CODE_REGEX, text):
        return True
    if re.search(DOCUMENT_NUMBER_REGEX, text):
        return True
    if text == "MALE" or text == "FEMALE":
        return True


def export(path, name, data):
    file_name = f"{path}/{name}_result.{FILE_EXT}"

    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        for key, value in data.items():
            writer.writerow([key, value])


def export_data_to_csv(full_path, data):
    path = os.path.dirname(full_path)
    name = pathlib.Path(full_path).stem
    export(path, name, data)
