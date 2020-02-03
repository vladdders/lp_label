import os
import tkinter
import string
import random

import cv2
from PIL import Image, ImageTk


ORIGIN_FOLDER = "raw"
DESTINATION_FOLDER = "results"
CONTENTS = [os.path.join(ORIGIN_FOLDER, i)
            for i in os.listdir(ORIGIN_FOLDER)
            if i.endswith(".jpg") or i.endswith(".png")]

print(CONTENTS)
UPSCALE_FACTOR = 3


if not len(CONTENTS):
    print(f"No files in {ORIGIN_FOLDER} folder, exiting.")
    exit()


def on_action(func):
    def wrapper(self, *arg, **kw):
        func(self, *arg, **kw)
        try:
            self.current_file = next(self.files)
        except StopIteration:
            print(f"{ORIGIN_FOLDER} empty, exiting.")
            exit(0)
        self.display_image(self.current_file)
    return wrapper


class App(tkinter.Frame):
    def __init__(self,*args,**kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)

        self.files = App.path_generator(folder=CONTENTS)
        self.setup()
        self.current_file = next(self.files)
        self.display_image(self.current_file)

    def setup(self):
        self.Label = tkinter.Label(self)
        self.Label.grid(row=0, column=0)
        self.Button = tkinter.Button(self, text="Delete", command=self.delete_photo)
        self.Button.grid(row=0,column=1)
        self.Entry = tkinter.Entry(self)
        self.Entry.bind('<Return>', self.label_photo)
        self.Entry.grid(row=1, column=0)
        self.TextLabel = tkinter.Label(self, text="enter label and press enter")
        self.TextLabel.grid(row=1, column=1)

    def display_image(self, image_path):
        image_object = Image.open(image_path)
        width, height = image_object.size

        resized_image_object = image_object.resize(
            (UPSCALE_FACTOR * width, UPSCALE_FACTOR * height),
            Image.NEAREST
        )

        photo_image = ImageTk.PhotoImage(resized_image_object)
        self.Label.config(image=photo_image)
        self.Label.image = photo_image

    @on_action
    def delete_photo(self):
        os.remove(self.current_file)

    @on_action
    def label_photo(self, event=None):

        label = self.Entry.get()
        if label == '':
            print("empty label, skipping")
            return
        print(f"assigning label {label}.")

        image = cv2.imread(self.current_file)

        rand = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

        new_image_path = os.path.join(
            DESTINATION_FOLDER, f"{label}_{rand}.jpg")

        cv2.imwrite(new_image_path, image)

        if os.path.isfile(new_image_path):
            os.remove(self.current_file)

        self.Entry.delete(0, 'end')

    @staticmethod
    def path_generator(folder=None):
        for file in folder:
            yield file


if __name__ == "__main__":
   root = tkinter.Tk()
   my_app = App(root)
   my_app.grid(row=0,column=0)
   root.mainloop()