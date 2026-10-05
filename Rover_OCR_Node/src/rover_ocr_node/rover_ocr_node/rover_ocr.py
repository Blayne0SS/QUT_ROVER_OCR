import threading
import easyocr
import numpy as np
import cv2 as cv
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import rclpy
from rclpy.node import Node


# These labels are created when the slideshow window starts.
Original_image_label = None
Altered_image_label = None

# The original image, marked image and OCR result at each position belong together.
image_array = []
Alter_OCR_Result_Array = []
OCR_Result_Array = []

# Images shown in the slideshow are resized to these dimensions.
Height = 680
Width = 645

# These values set the starting size of the image labels in the GUI.
GUI_Width = 80
GUI_Height = 40

# The slideshow uses positions starting at 1 when an image is selected.
index =1

# EasyOCR is used to check each selected camera frame for text.
# Project: https://github.com/JaidedAI/EasyOCR
reader = easyocr.Reader(['en'], True)

#function for the forward button
def Forward_Button():
    """Show the next image and its OCR result, if one is available."""
    global OCR_Result_Array
    global index
    global Original_image_label
    global Altered_image_label
    global image_array
    
    # Keep the slideshow index at 1 or above when the button is pressed.
    if index ==0:
        index =1
    
    # Only move forward when another OCR result has been stored.
    if index < len(OCR_Result_Array):
        Original_image_label.config(image=image_array[index])
        Altered_image_label.config(image=Alter_OCR_Result_Array[index])

        OCR_Text.set(OCR_Result_Array[index][0][1])
        OCR_Location_Text.set(OCR_Result_Array[index][0][0])

        # The arrays start at 0, so increase the displayed image number afterwards.
        index = index + 1
        current_image_number.set(index)

def Backwards_Button():
     """Show the previous image and its OCR result, if one is available."""
    global index
    global Original_image_label
    global Altered_image_label
    global OCR_Result_Array
    global image_array

    #The first image is position 1 in the slideshow, so do not move below it.
    if index >1:
        index = index - 1 
        
        Original_image_label.config(image=image_array[index-1])
        Altered_image_label.config(image=Alter_OCR_Result_Array[index-1])

        OCR_Text.set(OCR_Result_Array[index-1][0][1])
        OCR_Location_Text.set(OCR_Result_Array[index-1][0][0])
        current_image_number.set(index)


def Slide_Show():
    """Create the Tkinter window used to view images and OCR results."""
    global Original_image_label
    global Altered_image_label 
    
    root = tk.Tk()

    global image_array
    global OCR_Result_Array
    global Alter_OCR_Result_Array
    global index
    index = 0

    root.title("Image Slide Show")
    root.geometry("1480x800")

    global OCR_Text
    OCR_Text = tk.StringVar()

    global OCR_Location_Text
    OCR_Location_Text = tk.StringVar()

    global current_image_number
    current_image_number = tk.IntVar()
    current_image_number.set(index)

    # Create one frame for the original image and one for the image with a box.
    Original_image = ttk.Frame(root, borderwidth=7, relief="ridge", width=GUI_Width, height=GUI_Height)

    Altered_image = ttk.Frame(root, borderwidth=7, relief="ridge", width=GUI_Width, height=GUI_Height)
   
    Original_image_label = tk.Label(Original_image, width=GUI_Width, height=GUI_Height)
    Original_image_label.pack(fill=tk.BOTH, expand=False)

    Altered_image_label = tk.Label(Altered_image, width=GUI_Width, height=GUI_Height)
    Altered_image_label.pack(fill=tk.BOTH, expand=False)
   
    current_image_number_label = tk.Label(root, textvariable=current_image_number)

    Left = ttk.Button(root, text="<",command=Backwards_Button)
    Right = ttk.Button(root, text=">",command=Forward_Button)

    Result_text = ttk.Label(root, textvariable=OCR_Text)
    Location_text = ttk.Label(root, textvariable=OCR_Location_Text)

    Original_image.grid(column=1, row=1, columnspan=2, rowspan=3)
    Altered_image.grid(column=4, row=1, columnspan=2, rowspan=3)

    Left.grid(column=0, row=2, columnspan=1, rowspan=1)
    Right.grid(column=6, row=2, columnspan=1, rowspan=1)

    Result_text.grid(column=2, row=5, columnspan=3, rowspan=1)
    Location_text.grid(column=2, row=7, columnspan=3, rowspan=1)
    current_image_number_label.grid(column=2, row=8, columnspan=3, rowspan=1)

    # Start camera capture after the window has been created, then run Tkinter.
    root.after(10, camera)
    root.mainloop()


def camera():
    """Read camera frames and run OCR on every 120th frame."""
    global index
    global Original_image_label
    global Altered_image_label 
    global image_array 
    global OCR_Result_Array
    global Alter_OCR_Result_Array 

    # Camera 0 is the computer's default camera. Change this for the rover camera.
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Couldn't open camera")
        return

    count = 0
    
    def Frame_Capture_and_Proccessing():
        nonlocal count
        count += 1
        ret, frame = cap.read()
        Array_Number=0
        
        # OCR is run on every 120th frame to reduce how often the image is processed.
        if ret and count % 120 == 0:
            OCR_Reader_Result = reader.readtext(image=frame, paragraph=True)

            if OCR_Reader_Result:
               # Store the first result when text is detected for the first time.
                if OCR_Reader_Result[0][1] != "" and len(OCR_Result_Array) == 0:
                    print("Image is added")

                    # Copy the frame and draw a rectangle around the detected text.
                    image_data = np.asarray(frame)
                    img_copy = image_data.copy()
                    cv.rectangle(img_copy, OCR_Reader_Result[0][0][0], OCR_Reader_Result[0][0][2], (0, 255, 0), 5)

                    # Convert both versions of the frame to images for Tkinter.
                    alt_img = Image.fromarray(img_copy, "RGB")
                    alt_img = alt_img.resize((Width, Height), resample=3)
                    alt_img = ImageTk.PhotoImage(alt_img)

                    img_pil = Image.fromarray(frame) 
                    img_resized = img_pil.resize((Width, Height), resample=3)  
                    img_tk = ImageTk.PhotoImage(img_resized)  

                    # Keep the images and OCR data for later slideshow navigation.
                    image_array.append(img_tk)
                    Alter_OCR_Result_Array.append(alt_img)
                    OCR_Result_Array.append(OCR_Reader_Result)

                    # Display the first stored image and its OCR text.
                    if len(OCR_Result_Array)==1:   
                        index=1
                        Original_image_label.configure(image=image_array[0],width=Width, height=Height)
                        Altered_image_label.configure(image=Alter_OCR_Result_Array[0], width=Width, height=Height)
                        current_image_number.set(index)
                        OCR_Text.set(OCR_Result_Array[0][0][1])
                        OCR_Location_Text.set(str(OCR_Result_Array[0][0][0]))
                        
                else:
                    # Compare the detected text with the results already stored.
                    for OCR_Result_Array_Data in OCR_Result_Array:
                        print("Searching array")
                        
                        if OCR_Result_Array_Data[0][1]==OCR_Reader_Result[0][1]:
                            print("data not stored,data match detected")
                            break
                        

                        elif Array_Number==len(OCR_Result_Array)-1 and OCR_Result_Array_Data[0][1]!=OCR_Reader_Result[0][1]:
                             # This text is new, so prepare and store the frame.
                            image_data = np.asarray(frame)
                            img_copy = image_data.copy()
                            cv.rectangle(img_copy, OCR_Reader_Result[0][0][0], OCR_Reader_Result[0][0][2], (0, 255, 0), 5)

                            alt_img = Image.fromarray(img_copy, "RGB")
                            alt_img = alt_img.resize((Width, Height), resample=3)
                            alt_img = ImageTk.PhotoImage(alt_img)

                            img_pil = Image.fromarray(frame)  
                            img_resized = img_pil.resize((Width, Height), resample=3)  
                            img_tk = ImageTk.PhotoImage(img_resized)  
                            
                           # Store the images and OCR result at matching positions.
                            image_array.append(img_tk)
                            Alter_OCR_Result_Array.append(alt_img)
                            OCR_Result_Array.append(OCR_Reader_Result)

                            print("data stored, image number " + str(Array_Number))
                        Array_Number=Array_Number+1
            else:
                print("No text detected in the image.")

        # Schedule the next frame capture after 10 milliseconds.
        Original_image_label.after(10, Frame_Capture_and_Proccessing)
        
    # Begin capturing and processing frames.
    Frame_Capture_and_Proccessing()

class rover_ocr(Node):
    """ROS 2 node that starts the image slideshow in a separate thread."""
    
    def __init__(self):
        super().__init__('rover_ocr')
        Slide_Show_thread = threading.Thread(target=Slide_Show)
        Slide_Show_thread.start()

def main():
    """Initialise ROS 2 and keep the rover OCR node running."""
    rclpy.init()
    node = rover_ocr()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
