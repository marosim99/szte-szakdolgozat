import cv2
import easyocr
import pandas

pandas.set_option('display.max_rows', 100)
pandas.set_option('display.max_columns', 100)
pandas.set_option('display.width', 1000)

ID_CARD_PATH = "test_images/example_id_card.png"


def generate_image_with_bounding_boxes_on_words(ocr_result):
    img = cv2.imread(ID_CARD_PATH)

    for text_row in ocr_result:
        bottom_left = tuple(text_row[0][0])
        top_right = tuple(text_row[0][2])
        img = cv2.rectangle(img, bottom_left, top_right, (0, 255, 0), 10)

    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.imshow("output", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    reader = easyocr.Reader(['en'], gpu=False)
    data = reader.readtext(ID_CARD_PATH)
    data_frame = pandas.DataFrame(data, columns=['bbox', 'text', 'conf'])
    print(data_frame)
    generate_image_with_bounding_boxes_on_words(data)

