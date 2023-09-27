import os
from shutil import copy
import customtkinter as ctk
import threading
import parser
from PIL import Image


class SteamAssetsGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title('SteamAssets')
        self.wm_iconbitmap('steam.ico')
        self.protocol('WM_DELETE_WINDOW', self.on_close)
        self.bind_all('<Button-1>', lambda event: event.widget.focus_set())
        self.bind('<Left>', self.show_previous_image)
        self.bind('<Right>', self.show_next_image)

        id_label = ctk.CTkLabel(self, text='Enter ID of Steam App', text_color='white')
        id_label.pack(anchor='w')

        # Create a validation function to allow only digits
        validate_digits = self.register(self.validate_digits)

        self.id_entry = ctk.CTkEntry(self, validate="key", validatecommand=(validate_digits, '%P'))
        self.id_entry.pack(anchor='w')

        search_button = ctk.CTkButton(self, text='Search', command=self.start_search_func)
        search_button.pack(anchor='w', pady=20)

        self.progress_bar = ctk.CTkProgressBar(self, mode='indeterminate')

        self.image_index = 0
        self.images = []
        self.images_names = []
        self.image_labels = []

    def validate_digits(self, new_value):
        # Validate function to allow only digits
        if new_value.isdigit() or new_value == '':
            return True
        else:
            return False

    def start_search_func(self):
        self.show_progress_bar()
        self.progress_bar.start()

        # Start test_func in a separate thread
        thread = threading.Thread(target=self.search_func)
        thread.start()

    def search_func(self):
        self.images = []  # Clear existing images
        for url in parser.find_available_alt_assets(self.id_entry.get()):
            image = parser.download_image(url, 'temp')
            if image:
                self.images.append(image)
                self.images_names.append(url.split('/')[-1].split('.')[0])

        self.show_images()
        self.progress_bar.stop()
        self.hide_progress_bar()

    def hide_progress_bar(self):
        self.progress_bar.pack_forget()

    def show_progress_bar(self):
        self.progress_bar.pack(padx=10, pady=10)

    def show_images(self):
        # Clear existing image labels
        for label in self.image_labels:
            label.pack_forget()

        # Display the current image, title, and navigation buttons
        if self.images:
            current_image = Image.open(self.images[self.image_index])
            current_image = ctk.CTkImage(current_image, size=current_image.size)

            image_label = ctk.CTkLabel(self, image=current_image, text='')
            image_label.image = current_image
            image_label.pack(anchor='center')

            title_label = ctk.CTkLabel(self, text=self.images_names[self.image_index])
            title_label.pack(anchor='center')

            save_button = ctk.CTkButton(self, text='Save', command=self.save_image)
            save_button.pack(anchor='center')

            prev_button = ctk.CTkButton(self, text='Previous', command=self.show_previous_image)
            prev_button.pack(side='left')

            next_button = ctk.CTkButton(self, text='Next', command=self.show_next_image)
            next_button.pack(side='right')

            # Store the labels to remove them later
            self.image_labels = [image_label, title_label, save_button, prev_button, next_button]

    def show_next_image(self, *args):
        if self.images and self.image_index < len(self.images) - 1:
            self.image_index += 1
            self.show_images()

    def show_previous_image(self, *args):
        if self.images and self.image_index > 0:
            self.image_index -= 1
            self.show_images()

    def save_image(self):
        if self.images:
            file_name = self.images[self.image_index]
            file_name = os.path.basename(file_name)
            copy(os.path.join('temp', file_name), os.path.join('downloads', file_name))

    def on_close(self):
        for file in os.listdir('temp'):
            os.remove(os.path.join('temp', file))
        self.destroy()

if __name__ == '__main__':
    app = SteamAssetsGUI()
    app.mainloop()
