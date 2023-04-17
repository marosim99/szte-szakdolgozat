import easyocr
import customtkinter
from Utils import KeyValuePairFinder as kvpFinder
from Utils import ImagePreprocessor
from Utils import helpers

READER = easyocr.Reader(['en'], gpu=False)


def begin():
    message = customtkinter.CTkLabel(master=frame, text="Please wait until process finishes")
    message.pack(pady=12, padx=10)

    id_card_path = customtkinter.filedialog.askopenfilename(filetypes=[("Image File", '.jpg .png .jpeg .gif .pdf')])

    image = ImagePreprocessor.preprocess_image(id_card_path)
    data = READER.readtext(image)
    # helpers.generate_image_with_bounding_boxes_on_words(data, id_card_path)
    text_items = helpers.get_text_items_from_ocr_data(data)
    # helpers.print_card_text_items(text_items)
    #print("/-- OCR process finished --/")


    kvpFinder.find_key_value_pairs(text_items)
    #print("/-- Key-Value pair finding process finished --/")
    items_dict = helpers.items_to_dict(text_items)
    #print("/-- Formatted values: --/")
    post_processed_values = helpers.post_process_text(items_dict)
    helpers.print_dict(post_processed_values)
    helpers.export_data_to_csv("", post_processed_values)

    message = customtkinter.CTkLabel(master=frame, text="Process finished, CSV file is saved in the folder of the source image")
    message.pack(pady=12, padx=10)

if __name__ == '__main__':
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("green")

    root = customtkinter.CTk()
    root.geometry("600x400")
    root.title("ID Card Digitalizer")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="Hello")
    label.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=frame, text="Start", command=begin)
    button.pack(pady=12, padx=10)

    checkbox = customtkinter.CTkCheckBox(master=frame, text="show image with recognized text")
    checkbox.pack(pady=12, padx=10)

    root.mainloop()




