# IMAGE COLORIZER AND GRAYSCALE CONVERTER
#### Video Demo:  <https://youtu.be/721H3f4UMPc?si=-Zam9uv7VcfvXiwg>
#### Description:

The Image Colorizer and Grayscale Converter is a desktop application built in Python that allows users to automatically colorize grayscale images using a deep learning model and convert colored images into grayscale. The project demonstrates how computer vision, neural networks, and graphical user interfaces can be combined to create an interactive image processing tool.

The application uses a pretrained deep learning model to predict realistic color values for grayscale images. Users can select an image from their computer, apply colorization, preview the result, and save the processed image. Additionally, the program includes a feature that converts colored images into grayscale for comparison and image processing purposes.

This project integrates OpenCV’s deep neural network module with a Tkinter-based graphical interface to provide a simple and accessible experience for users.

---

## Features

- Automatic Image Colorization
  Converts grayscale images into colored images using a pretrained deep learning model.

- Grayscale Conversion
  Allows users to convert colored images into grayscale using OpenCV image processing.

- Graphical User Interface
  A user-friendly interface built using Tkinter that allows users to easily interact with the application.

- Adjustable Colorization Intensity
  Includes a slider that lets users control the strength of the colorization effect.

- Image Preview Window
  Processed images are displayed in a separate window for easy viewing.

- Save Processed Images
  Users can save the processed images to their local system in common image formats.

---

## Technologies Used

The project uses the following technologies and libraries:

- Python – Primary programming language used to build the application.
- OpenCV – Used for image processing and deep neural network implementation.
- NumPy – Used for numerical operations and handling model data.
- Tkinter – Used to create the graphical user interface.
- Pillow (PIL) – Used to display images within the GUI.
- Caffe Model – Pretrained deep learning model used for image colorization.

---

## How It Works

### Image Colorization

The application uses a pretrained deep learning model trained on large datasets of colored images. When a grayscale image is selected, the following steps occur:

1. The image is loaded using OpenCV.
2. The image is converted into the LAB color space.
3. The luminance channel (L) is extracted.
4. The neural network predicts the missing color channels (A and B).
5. The predicted color channels are combined with the luminance channel.
6. The image is converted back into a standard color format and displayed.

This process produces a realistic colorized version of the original grayscale image.

### Grayscale Conversion

For colored images, the application can convert them into grayscale using OpenCV's color conversion function. This removes the color information and retains only brightness values.

### Intensity Adjustment

The intensity slider allows users to control how strong the predicted colors appear in the final image. Lower values produce softer and more subtle colors, while higher values create more vibrant and saturated colors.

---


## Usage

1. Run the Python script.
2. Click the Browse button to select an image from your computer.
3. Choose one of the following options:
   - Colorize Image to convert a grayscale image into a colored image.
   - Convert to Grayscale to convert a colored image into grayscale.
4. Adjust the intensity slider to control the color strength.
5. Preview the processed image in the new window.
6. Click Save Image if you want to store the processed result.

---

## Future Improvements

Some possible improvements for the project include:

- Supporting batch processing for multiple images
- Adding before-and-after comparison views
- Allowing users to upload images directly within the application
- Adding additional image filters and enhancement tools
- Improving the user interface design

---

## Acknowledgments

This project was completed as part of the CS50x course.
ChatGPT was used as a supplementary tool for debugging assistance, explanations, and improving the structure of the project.
