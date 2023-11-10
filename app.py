# Import necessary libraries
import tkinter as tk
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mobilenetv2_preprocess_input
from tkinter import font
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Load the pre-trained MobileNetV2 model
model = tf.keras.models.load_model('model/mobilenetv2_nn_model.h5')

# Define the function to preprocess the image and predict its class
def classify_image(image_path):
    """Preprocess the image and predict the class."""
    # Load the image with the target size required by MobileNetV2
    image = Image.open(image_path)
    image = image.resize((224, 224))
    
    # Convert the image to a numpy array and preprocess it
    image_array = np.array(image)
    image_array = mobilenetv2_preprocess_input(image_array)
    image_array = np.expand_dims(image_array, axis=0)
    
    # Predict the probability of the image being a dog
    probability = model.predict(image_array).flatten()[0]
    class_label = 'Dog' if probability > 0.5 else 'Cat'
    
    # Return the class label
    return class_label

# Define the GUI function for image upload and display
def upload_image():
    """Handle image uploading and display."""
    # Get the image file path from the user
    file_path = filedialog.askopenfilename()
    
    # Proceed only if a file has been selected
    if file_path:
        # Open, display, and classify the image
        uploaded_image = Image.open(file_path)
        uploaded_image.thumbnail((224, 224))  # Resize for display in the app without altering its aspect ratio
        uploaded_image_tk = ImageTk.PhotoImage(uploaded_image)
        label.config(image=uploaded_image_tk)
        label.image = uploaded_image_tk
        result.set("Classifying...")
        classification_result = classify_image(file_path) 
        result.set("Result: " + classification_result)
    else:
        messagebox.showwarning("Warning", "Please select an image to classify.")

# Initialize the main window of the application
root = tk.Tk()
root.title("Dog vs Cat Classifier")
root.geometry('400x300') 

# Setup the main frame for the GUI elements
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Label to display the uploaded image
label = tk.Label(frame)
label.pack(pady=5)

# Button that allows the user to upload an image
button = tk.Button(frame, text="Select Image", command=upload_image)
button.pack(pady=5)

# Label to show the classification result
result = tk.StringVar()
result_font = tk.font.Font(family='Helvetica', size=16) 
result_label = tk.Label(frame, textvariable=result, font=result_font)
result_label.pack(pady=5)

# Run the GUI application
root.mainloop()