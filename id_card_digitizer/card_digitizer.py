import easyocr
import customtkinter
from Utils import KeyValuePairFinder as kvpFinder
from Utils import ImagePreprocessor
from Utils import helpers

READER = easyocr.Reader(['en'], gpu=False)


def write_message(message):
    message_label.configure(text=message)
    message_label.pack(pady=12, padx=10)
    root.update()


def read_image():
    return customtkinter.filedialog.askopenfilename(
        filetypes=[("Image File", '.jpg .png .tiff')])


def get_data_from_image(image):
    try:
        prepared_image = ImagePreprocessor.preprocess_image(image)
        return READER.readtext(prepared_image)
    except Exception:
        raise Exception("Error while preparing and reading data.")


def process_data(data):
    try:
        text_items = helpers.get_text_items_from_ocr_data(data)
        kvpFinder.find_key_value_pairs(text_items)
        return text_items
    except Exception:
        raise Exception("Error while processing data.")


def post_process_data(text_items):
    try:
        items_dict = helpers.items_to_dict(text_items)
        return helpers.post_process_text(items_dict)
    except Exception:
        raise Exception("Error while post-processing data.")


def begin():
    try:
        id_card_path = read_image()
        if id_card_path:
            write_message("Process started, please wait...")

            image = ImagePreprocessor.read_image(id_card_path)
            data = get_data_from_image(image)
            text_items = process_data(data)

            post_processed_values = post_process_data(text_items)
            helpers.export_data_to_csv(id_card_path, post_processed_values)

            write_message("Process finished, CSV file saved to folder of the source image.")

            if show_image.get() == 1:
                helpers.draw_bounding_boxes(data, text_items, image)
    except Exception as ex:
        write_message(f"Something went wrong: {ex}")


# RUN THIS METHOD TO START THE APPLICATION
if __name__ == '__main__':
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("green")

    root = customtkinter.CTk()
    root.geometry("1040x500")
    root.title("ID Card Digitizer")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=40, fill="both", expand=True)

    label = customtkinter.CTkLabel(
        master=frame, text="Begin process with selecting a scanned ID card", font=(None, 40))
    label.pack(pady=24, padx=10)

    button = customtkinter.CTkButton(
        master=frame, text="Select Image & Start Process", command=begin, font=(None, 32))
    button.pack(pady=24, padx=10)

    show_image = customtkinter.IntVar()
    checkbox = customtkinter.CTkCheckBox(
        master=frame, text="Show image with recognized text", variable=show_image, font=(None, 18))
    checkbox.pack(pady=24, padx=10)

    message_label = customtkinter.CTkLabel(master=frame, text="", font=(None, 30), text_color="green")
    message_label.pack(pady=24, padx=10)

    root.mainloop()
