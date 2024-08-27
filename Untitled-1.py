

#Imported modules (Done using pip, check docs for pip commands)
import easyocr
import torch 

#modules included in python 
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt 


from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

#sets the reader to be able to read english
#Futher configuratio options are located on a webpage whoses link
#is stored in documentation
reader = easyocr.Reader(['en'],True)


image_array = []
Alter_OCR_Result_Array = []

OCR_Result_Array = []
location_array = []
test_images_Array=[]
test_images_OCR_Array=[]



Height= 810
Width=800

#print('X_data shape:', np.array(X_data).shape) 
# Image print https://stackoverflow.com/questions/37747021/create-numpy-array-of-images



def Forward_Button():




    global OCR_Result_Array
    global index
    global Oringal_image_label
    global Altered_image_label
    global image_array
    


    if index +1 < len(OCR_Result_Array):
        index = index + 1
        print("forward button activated " + str(index))

        Oringal_image_label.config(image=image_array[index])
        Altered_image_label.config(image=Alter_OCR_Result_Array[index])

        OCR_Text.set(OCR_Result_Array[index][0][1])
        OCR_Location.set(OCR_Result_Array[index][0][0])
        current_image_number.set(index)
        
    


 
    

def Backwards_Button():
    global index
    global Oringal_image_label
    global Altered_image_label
    global OCR_Result_Array
    global image_array

    if index !=0:
        index = index - 1 
        print("Backwards button activated " + str(index))
        
        Oringal_image_label.config(image=image_array[index])
        Altered_image_label.config(image=Alter_OCR_Result_Array[index])

        OCR_Text.set(OCR_Result_Array[index][0][1])
        OCR_Location.set(OCR_Result_Array[index][0][0])
        current_image_number.set(index)
        
        

#Function Slide_Show
#Function use to store and view post easyocr images
def Slide_Show():

    root = Tk()
    
    global image_array

    global OCR_Result_Array

    global Alter_OCR_Result_Array
    
    
    
    


    #Test images
    img = Image.open("/home/blaynev2/Desktop/Rover_OCR/new-qld-number-plate.jpg")
    OCR_Reader(img)


    img = Image.open("/home/blaynev2/Desktop/Rover_OCR/2002_QLD_Numberplate_374.jpg")
    OCR_Reader(img)
    
    #use tkinter
    global index
    index=0


    #image_array[index]=ImageTk.PhotoImage(image_array[index].resize((Width,Height) , resample=3))
    
    
    root.title("Image Slide Show")
    content = ttk.Frame(root)
  
    global Oringal_image_label
    global Altered_image_label


    global OCR_Text
    OCR_Text = StringVar()
    OCR_Text.set(OCR_Result_Array[index][0][1])


    global OCR_Location
    OCR_Location = IntVar()
    OCR_Location.set(OCR_Result_Array[index][0][0])
   
    global current_image_number
    current_image_number = IntVar()
    current_image_number.set(index)

    Oringal_image = ttk.Frame(content, borderwidth=7, relief="ridge", width=Width, height=Height)
    Altered_image = ttk.Frame(content,borderwidth=7, relief="ridge", width=Width, height=Height)
    
    Oringal_image_label = Label(Oringal_image,width=Width, height=Height,
                                image=image_array[index])
    Oringal_image_label.pack
    
    Altered_image_label = Label(Altered_image,width=Width, height=Height,
                                image=Alter_OCR_Result_Array[index])
                            
    Altered_image_label.pack

    current_image_number_label= Label(content, textvariable=current_image_number)

    Left = ttk.Button(content, text="<",command=Backwards_Button)
    Right = ttk.Button(content, text=">",command=Forward_Button)

    Result_text=ttk.Label(content, textvariable=OCR_Text)
    Location_text=ttk.Label(content, textvariable= OCR_Location)

    content.grid(column=0, row=0)
    Oringal_image.grid(column=1, row=1, columnspan=2, rowspan=3)
    Altered_image.grid(column=4, row=1, columnspan=2,rowspan=3)
    
    Left.grid(column=0, row=2, columnspan=1,rowspan=1)
    Right.grid(column=6, row=2, columnspan=1,rowspan=1)
    
    Result_text.grid(column=2, row=5, columnspan=3,rowspan=1)
    Location_text.grid(column=2, row=7, columnspan=3,rowspan=1)

    current_image_number_label.grid(column=2, row=8, columnspan=3,rowspan=1)


    Oringal_image_label.grid(column=1, row=1, columnspan=2, rowspan=3)
    Altered_image_label.grid(column=4, row=1, columnspan=2,rowspan=3)
    
    root.mainloop()


#Function OCR_Reader
#Function uses easyocr to check if characters are present in an image
#and 
def OCR_Reader(img):
    print("Activated")
    #details=0 for only Text
    OCR_Reader_Result = reader.readtext(image=img,paragraph=True)
    
    #Prints location
    #print(OCR_Reader_Result[0][0])
    
    #prints Text
    #print(OCR_Reader_Result[0][1])
    
    #Prints all information
    print(str(OCR_Reader_Result))


    global image_array

    global OCR_Result_Array

    global Alter_OCR_Result_Array 



    
    #The following code determines if the image will be added to the tbe OCR_Result_Array
    #For the first image to be added text has to be detected
    #For addition images to be added, text that does not appear in previous imges will need to be detected
    #
    #Data stores text data in OCR_Result_Array
    #     stores images in image_array
    #Note:Assumptions
    #       All texts will be different

    


    Array_Number=0
    if(OCR_Reader_Result[0][1]!= None and len(OCR_Result_Array)==0):
        print("Image is added")
        print(OCR_Reader_Result[0][0][0])
        print(OCR_Reader_Result[0][0][2])
        
        #altered image array
        image_data = np.asarray(img)
        img_copy = image_data.copy()
        cv.rectangle(img_copy, OCR_Reader_Result[0][0][0],OCR_Reader_Result[0][0][2],(0,255,0),5)

        alt_img=Image.fromarray(img_copy,"RGB")
        alt_img= ImageTk.PhotoImage(alt_img.resize((Width,Height),resample=3))
        Alter_OCR_Result_Array.append(alt_img)
        
        #image array
        img= ImageTk.PhotoImage(img.resize((Width,Height)))
        image_array.append(img)
        

        
        
        OCR_Result_Array.append(OCR_Reader_Result)

    
     
       


    else:
        print("for loop activated")
        for OCR_Result_Array_Data in OCR_Result_Array:
            print("for loop active")
            print(Array_Number)
            if OCR_Result_Array_Data[0][1]==OCR_Reader_Result[0][1]:
                print("data not stored")
                break
            elif Array_Number==len(OCR_Result_Array)-1 and OCR_Result_Array_Data[0][1]!=OCR_Reader_Result[0][1]:

                
                image_data = np.asarray(img)
                img_copy = image_data.copy()
                cv.rectangle(img_copy, OCR_Reader_Result[0][0][0],OCR_Reader_Result[0][0][2],(0,255,0),5)

                alt_img=Image.fromarray(img_copy,"RGB")
                alt_img= ImageTk.PhotoImage(alt_img.resize((Width,Height),resample=3),)
                Alter_OCR_Result_Array.append(alt_img)



                img= ImageTk.PhotoImage(img.resize((Width,Height) , resample=3))
                image_array.append(img)
                OCR_Result_Array.append(OCR_Reader_Result)
                print("data stored, image number " + str(Array_Number))
            Array_Number=Array_Number+1






    


def OCR_Reader_activated(img):
    print("OCR_Reader_activated")
   
#Function camera
#activates camera, presents view and calls OCR_Reader
#

def camera():

    cap = cv.VideoCapture(0)
    #if not cap.isOpened():
    #        print("Cannot open camera")
    #        exit()
    
    count = 0
    while True: 
       
        ret,img=cap.read()
        cv.imshow('Video',img)

        count=count+1
        
        
        if(count % 120==0):
            print(str(count))
            OCR_Reader(img)


        if cv.waitKey(1) == ord('q'):
             cv.destroyAllWindows() 
             cv.VideoCapture(0).release()
             break
      
    
        

        
        

#camera()
Slide_Show()




print(cv.__version__)

