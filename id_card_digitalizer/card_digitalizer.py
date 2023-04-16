import easyocr
from Utils import KeyValuePairFinder as kvpFinder
from Utils import ImagePreprocessor
from Utils import helpers

ID_CARD_PATH = "example_id_card.png"
READER = easyocr.Reader(['en'], gpu=False)


if __name__ == '__main__':
    image = ImagePreprocessor.preprocess_image(ID_CARD_PATH)
    data = READER.readtext(image)
    # helpers.generate_image_with_bounding_boxes_on_words(data, ID_CARD_PATH)
    text_items = helpers.get_text_items_from_ocr_data(data)
    # helpers.print_card_text_items(text_items)
    print("/-- OCR process finished --/")

    kvpFinder.find_key_value_pairs(text_items)
    print("/-- Key-Value pair finding process finished --/")
    items_dict = helpers.items_to_dict(text_items)
    helpers.print_dict(items_dict)
    print("/-- Formatted values: --/")
    post_processed_values = helpers.post_process_text(items_dict)
    helpers.print_dict(post_processed_values)



