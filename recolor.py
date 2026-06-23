import numpy as np
import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# NOTE: This project was completed with supplementary guidance from ChatGPT.

DIR = r"C:\Users\Welcome\Documents\colorize"
PROTOTXT = os.path.join(DIR, r"model/colorization_deploy_v2.prototxt")
POINTS = os.path.join(DIR, r"model/pts_in_hull.npy")
MODEL = os.path.join(DIR, r"model/colorization_release_v2.caffemodel")

print('Loading Model')
net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
pts = np.load(POINTS)

class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2,313,1,1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def colorize_image(path, intensity=1.0):
    image = cv2.imread(path)
    scaled = image.astype("float32")/255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    print("Colorizing the image")
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab * intensity), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")

    return image, colorized

def convert_to_grayscale(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, gray_image

def create_collage(original, processed):
    original = cv2.resize(original, (300, 300))
    processed = cv2.resize(processed, (300, 300))
    collage = np.hstack((original, cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR) if len(processed.shape) == 2 else processed))
    return collage


class ImageProcessorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Colorizer and Grayscale Converter")
        self.geometry("800x600")
        self.configure(bg="#333333")
        self.image_path = tk.StringVar()
        self.intensity = tk.DoubleVar(value=1.0)
        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.title_label = tk.Label(self, text="Image Colorizer and Grayscale Converter", 
                                    font=("Arial", 24), fg="white", bg="#333333")
        self.title_label.pack(pady=20)

        self.path_entry = tk.Entry(self, textvariable=self.image_path, width=50)
        self.path_entry.pack(pady=10)

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_image, 
                                       bg="#555555", fg="white")
        self.browse_button.pack(pady=5)

        self.colorize_button = tk.Button(self, text="Colorize Image", command=self.colorize_action, 
                                         bg="#0066CC", fg="white")
        self.colorize_button.pack(pady=10)

        self.grayscale_button = tk.Button(self, text="Convert to Grayscale", command=self.grayscale_action, 
                                          bg="#0066CC", fg="white")
        self.grayscale_button.pack(pady=10)

        self.intensity_scale = tk.Scale(self, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, 
                                        label="Intensity", variable=self.intensity, bg="#333333", fg="white")
        self.intensity_scale.pack(pady=20)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit, bg="#CC0000", fg="white")
        self.quit_button.pack(pady=20)

    def browse_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path.set(file_path)

    def colorize_action(self):
        image_path = self.image_path.get()
        if not image_path:
            messagebox.showerror("Error", "Please select an image file.")
            return
        try:
            _, colorized = colorize_image(image_path, self.intensity.get())
            self.show_image(colorized)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to colorize image: {str(e)}")

    def grayscale_action(self):
        image_path = self.image_path.get()
        if not image_path:
            messagebox.showerror("Error", "Please select an image file.")
            return
        try:
            _, gray_image = convert_to_grayscale(image_path)
            self.show_image(gray_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert to grayscale: {str(e)}")

    def show_image(self, image):
            def on_save():
                file_path = filedialog.asksaveasfilename(defaultextension=".jpg", 
                                                         filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
                if file_path:
                    cv2.imwrite(file_path, image)
                    messagebox.showinfo("Success", "Your image has been saved successfully")

            max_width, max_height = 600, 400 

            h, w = image.shape[:2]
            scale = min(max_width / w, max_height / h)
            new_w, new_h = int(w * scale), int(h * scale)
            resized_image = cv2.resize(image, (new_w, new_h))

            window = tk.Toplevel()
            window.title("Processed Image")
            canvas = tk.Canvas(window, width=new_w, height=new_h)
            canvas.pack()
            if len(resized_image.shape) == 3:
              img = Image.fromarray(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
            else:
              img = Image.fromarray(resized_image)
            img_tk = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            canvas.image = img_tk  # keep reference
            save_button = tk.Button(window, text="Save Image", command=on_save)
            save_button.pack(pady=10)


if __name__ == "__main__":
    app = ImageProcessorApp()
    app.mainloop()
