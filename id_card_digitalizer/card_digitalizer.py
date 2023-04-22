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
        filetypes=[("Image File", '.jpg .png .jpeg .gif .pdf')])


def begin():
    try:
        id_card_path = read_image()

        write_message("Process started, please wait...")

        image = ImagePreprocessor.read_image(id_card_path)
        prepared_image = ImagePreprocessor.preprocess_image(image)
        data = READER.readtext(prepared_image)

        text_items = helpers.get_text_items_from_ocr_data(data)
        kvpFinder.find_key_value_pairs(text_items)

        if show_image.get() == 1:
            helpers.draw_bounding_boxes(data, text_items, image)

        items_dict = helpers.items_to_dict(text_items)
        post_processed_values = helpers.post_process_text(items_dict)
        # helpers.print_dict(post_processed_values)
        helpers.export_data_to_csv(id_card_path, post_processed_values)
    except:
        write_message("An error happened, please try again.")
    else:
        write_message("Process finished, CSV file is saved in the folder of the source image.")


if __name__ == '__main__':
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("green")

    root = customtkinter.CTk()
    root.geometry("520x250")
    root.title("ID Card Digitalizer")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=40, fill="both", expand=True)

    label = customtkinter.CTkLabel(
        master=frame, text="Begin process with selecting a scanned ID card", font=(None, 20))
    label.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(
        master=frame, text="Select Document & Start Process", command=begin, font=(None, 16))
    button.pack(pady=12, padx=10)

    show_image = customtkinter.IntVar()
    checkbox = customtkinter.CTkCheckBox(
        master=frame, text="Show image with recognized text", variable=show_image)
    checkbox.pack(pady=12, padx=10)

    message_label = customtkinter.CTkLabel(master=frame, text="")
    message_label.pack(pady=12, padx=10)

    root.mainloop()
