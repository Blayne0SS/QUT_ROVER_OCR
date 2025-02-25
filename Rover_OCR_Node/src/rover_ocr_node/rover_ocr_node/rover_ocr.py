import threading
import easyocr
import numpy as np
import cv2 as cv
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk



import rclpy
from rclpy.node import Node




Original_image_label = None
Altered_image_label = None

#Data collected is stored in the following arrays 
image_array = []
Alter_OCR_Result_Array = []
OCR_Result_Array = []
location_array = []


#for image resizing 
Height = 680
Width = 645

#for GUI image label sizes
GUI_Width = 80
GUI_Height = 40

index =1

#easy OCR is the ocr plugin used to determine if text is presented in a image
#https://github.com/JaidedAI/EasyOCR 
reader = easyocr.Reader(['en'], True)



#function for the forward button
def Forward_Button():

    global OCR_Result_Array
    global index
    global Original_image_label
    global Altered_image_label
    global image_array
    
    #During testing index had the ability to start at 0 , to avoid this index is set to 1.
    
    if index ==0:
        index =1
    
    #print(str(index) + " index value ")
    #print(str( len(OCR_Result_Array)) + " array lens value ")

    #if index is less then  len(OCR_Result_Array which represents number of elements in te array
    #it means there is available data in the arrays
    if index < len(OCR_Result_Array):
        
        #print("forward button activated " + str(index))

        Original_image_label.config(image=image_array[index])
        Altered_image_label.config(image=Alter_OCR_Result_Array[index])

        OCR_Text.set(OCR_Result_Array[index][0][1])
        #print(OCR_Result_Array[index][0][1])
        OCR_Location_Text.set(OCR_Result_Array[index][0][0])

        #as arrays start at 0, index is increased after data is extracted from the array
        index = index + 1
        current_image_number.set(index)

        
    
 
    
#function for the backwards button
def Backwards_Button():
    global index
    global Original_image_label
    global Altered_image_label
    global OCR_Result_Array
    global image_array


    #uses to determine if index is above 1. minimum index is 1. 
    #therefore index-1 is used to select correct frames and ssoicated text
    if index >1:
        index = index - 1 
        
        Original_image_label.config(image=image_array[index-1])
        Altered_image_label.config(image=Alter_OCR_Result_Array[index-1])

        OCR_Text.set(OCR_Result_Array[index-1][0][1])
        #print(OCR_Result_Array[index-1][0][1])
        OCR_Location_Text.set(OCR_Result_Array[index-1][0][0])
        current_image_number.set(index)







#This function contains the configuration of the tinker GUI 
def Slide_Show():
    global Original_image_label
    global Altered_image_label 
    root = tk.Tk()

    global image_array
    global OCR_Result_Array
    global Alter_OCR_Result_Array
    global index
    index = 0

    #Title and GUI starting size
    root.title("Image Slide Show")
    root.geometry("1480x800")


    
    global OCR_Text
    OCR_Text = tk.StringVar()

    global OCR_Location_Text
    OCR_Location_Text = tk.StringVar()

    global current_image_number
    current_image_number = tk.IntVar()
    current_image_number.set(index)

    # Initialize the frames for displaying images
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

    # Update the UI periodically from the update queue
    root.after(10, camera)
    root.mainloop()

#The following section of code contains the ativation of the camera and the proccessing of the frame captured by the camera
#Currently the every 120th frame undergoes ocr 
def camera():
    global index
    global Original_image_label
    global Altered_image_label 

    global image_array 
    global OCR_Result_Array
    global Alter_OCR_Result_Array 

    #change setting to match the camera used by the rover
    #currently on 0 as it represents the camera used by a computer
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
        if ret and count % 120 == 0:
           
           
            OCR_Reader_Result = reader.readtext(image=frame, paragraph=True)

            if OCR_Reader_Result:
               
                #For first image with text within it. 
                if OCR_Reader_Result[0][1] != "" and len(OCR_Result_Array) == 0:
                    print("Image is added")

                    # Process the image and draw bounding box
                    image_data = np.asarray(frame)
                    img_copy = image_data.copy()
                    cv.rectangle(img_copy, OCR_Reader_Result[0][0][0], OCR_Reader_Result[0][0][2], (0, 255, 0), 5)

                    # Convert to PIL Image before resizing
                    alt_img = Image.fromarray(img_copy, "RGB")
                    alt_img = alt_img.resize((Width, Height), resample=3)
                    alt_img = ImageTk.PhotoImage(alt_img)

                    # Convert to PIL Image before resizing
                    img_pil = Image.fromarray(frame)  # Convert NumPy array to PIL Image
                    img_resized = img_pil.resize((Width, Height), resample=3)  # Resize using PIL
                    img_tk = ImageTk.PhotoImage(img_resized)  # Convert to Tkinter-compatible format

                    # Append to arrays for later use in Slide_Show
                    image_array.append(img_tk)
                    Alter_OCR_Result_Array.append(alt_img)
                    OCR_Result_Array.append(OCR_Reader_Result)


                    #When first image is detected, sends image and text to arrays and updates index.
                    # index is set to 1. 

                    if len(OCR_Result_Array)==1:   
                        index=1
                        Original_image_label.configure(image=image_array[0],width=Width, height=Height)
                        Altered_image_label.configure(image=Alter_OCR_Result_Array[0], width=Width, height=Height)
                        current_image_number.set(index)
                        OCR_Text.set(OCR_Result_Array[0][0][1])
                        OCR_Location_Text.set(str(OCR_Result_Array[0][0][0]))
                        


                else:

                    #print(str(Array_Number) + "array number") 

                    for OCR_Result_Array_Data in OCR_Result_Array:
                        print("Searching array")
                        
                        if OCR_Result_Array_Data[0][1]==OCR_Reader_Result[0][1]:
                            print("data not stored,data match detected")
                            break
                        

                        elif Array_Number==len(OCR_Result_Array)-1 and OCR_Result_Array_Data[0][1]!=OCR_Reader_Result[0][1]:
                            # Process the image and draw bounding box
                            image_data = np.asarray(frame)
                            img_copy = image_data.copy()
                            cv.rectangle(img_copy, OCR_Reader_Result[0][0][0], OCR_Reader_Result[0][0][2], (0, 255, 0), 5)

                            # Convert to PIL Image before resizing
                            alt_img = Image.fromarray(img_copy, "RGB")
                            alt_img = alt_img.resize((Width, Height), resample=3)
                            alt_img = ImageTk.PhotoImage(alt_img)

                            # Convert to PIL Image before resizing
                            img_pil = Image.fromarray(frame)  # Convert NumPy array to PIL Image
                            img_resized = img_pil.resize((Width, Height), resample=3)  # Resize using PIL
                            img_tk = ImageTk.PhotoImage(img_resized)  # Convert to Tkinter-compatible format


                            #adds image and text to arrays 
                            image_array.append(img_tk)
                            Alter_OCR_Result_Array.append(alt_img)
                            OCR_Result_Array.append(OCR_Reader_Result)


                            print("data stored, image number " + str(Array_Number))
                        Array_Number=Array_Number+1
            else:
                print("No text detected in the image.")

            # Update the label with the new image
            
            
        

        # Schedule the next frame update
        Original_image_label.after(10, Frame_Capture_and_Proccessing)
        

    # Start the frame update
    Frame_Capture_and_Proccessing()


#The following class contains the ros 2 node and slide show activation
#Slide show has its own thread to prevent issues between the camera and tinker GUI
class rover_ocr(Node):
    def __init__(self):
        super().__init__('rover_ocr')
        Slide_Show_thread = threading.Thread(target=Slide_Show)
        Slide_Show_thread.start()

        





#initates the node 
def main():
    rclpy.init()
    node = rover_ocr()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    

#activates the script
if __name__ == "__main__":
    main()
