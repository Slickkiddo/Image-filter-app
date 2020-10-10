#   IMAGE FILTER GUI
# import tkinter as tk
import tkinter.font as font
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Filter import BasicFilter
from PIL import Image

import numpy as np
import os
import cv2

import tkinter as tk

LARGE_FONT= ("Verdana", 12)

from PIL import Image, ImageTk, ImageDraw

#   16:9 ratios:: 1024x576, 1152x648, 1280x720, 1366x768, 1600x900, 1920x1080

class Application(Tk):
    
    order=2
    cutoff=50

    def __init__(self):
        super(Application, self).__init__()
        
        base_folder = os.path.dirname(__file__)
        image_path = os.path.join(base_folder, 'icon5.gif')

        #   SETTING UP MAIN CANVAS
        self.title("Photo Filter App")
        self.minsize(1024, 576)
        self.geometry("1920x1080")
        img = PhotoImage(file=image_path)
        self.iconphoto(False, img)
        canvas = Canvas(self)
        canvas.pack()

        self.fontSize = font.Font(size=25)

        #   QUADRANT OF FRAME PLACEMENT
        self.frame_q1 = Frame(self, bg='#202020')
        self.frame_q1.place(relx=.66, rely=0, relwidth=.33, relheight=.60)

        self.frame_q2 = Frame(self, bg='#101010')
        self.frame_q2.place(relx=0.33, rely=0, relwidth=0.33, relheight=0.60)

#         self.frame_q4 = Frame(self, bg='#ffffff')
#         self.frame_q4.place(relx=0, rely=.6, relwidth=0.3, relheight=1)
        
#         self.frame_q5 = Frame(self, bg='#505050')
#         self.frame_q5.place(relx=0.3, rely=.8, relwidth=1, relheight=1)
        
        

        #   CANVAS IMAGE PLACEMENT
        self.img_canvas_q2 = Canvas(self.frame_q2, bg='black')
        self.img_canvas_q2.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

        self.img_canvas_q1 = Canvas(self.frame_q1, bg='black')
        self.img_canvas_q1.place(relx=0, rely=0.1, relwidth=1, relheight=0.90)
        


        #   CONTAINER WHERE FRAMES ARE STACKED AND SHOWN BASED ON COMBOBOX OPTION
        middle_container = Frame(self)
        middle_container.place(relx=0, rely=.0, relwidth=0.33, relheight=0.6)

        #   FRAME QUADRANT 1 BUTTONS AND TOOLS
        self.filter_combo()
        self.select_filter_btn = Button(self.frame_q1, text='Select', padx=20 ,command=self.options_select).grid(row=0, column=1)

        #   FRAME QUADRANT 2 BUTTONS AND TOOLS
        self.upload_button = Image.open('upload_2.png')
        self.upload_button = self.upload_button.resize((200, 35), Image.ANTIALIAS)
        self.buttonImg = ImageTk.PhotoImage(self.upload_button)

        self.upload_button = Button(self.frame_q2, image=self.buttonImg, bg='#202020', command=self.fileInput) \
            .pack(side='top')

        #   FRAME QUADRANT 4 BUTTONS AND TOOLS

        #   MIDDLE FRAME BUTTONS AND TOOLS
        self.frames = {}
        for F in (FirstPage, ButterworthHighPage, ButterworthLowPage, GaussianHighPage, GaussianLowPage, OlympicPage, HomomorphicPage, IdealHighPage, IdealLowPage):
            page_name = F.__name__
            frame = F(parent=middle_container, controller=self)
            self.frames[page_name] = frame

            #   PLACE ALL PAGES IN SAME LOCATION
            frame.grid(row=0, column=1, sticky="nsew")

        self.show_frame("FirstPage")

    def show_frame(self, page_name):
        '''Show frame for the given page name'''

        frame = self.frames[page_name]
        frame.tkraise()

    #   QUADRANT 1 COMBOBOX FUNCTION
    def filter_combo(self):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.frame_q1, textvariable=self.box_value, width=30, state='readonly',
                                justify='center')
        self.box['values'] = ("SELECT FILTER", "Butterworth High", "Butterworth Low", "Gaussian High", "Gaussian Low", "Olympic", "Homomorphic", "Ideal High", "Ideal Low")
        self.box.grid(row=0, column=0)
        self.box.current(0)

    #   PRINT FILTER COMBOBOX VALUE
    def options_select(self):
        #   Print to Console for Debugging
        filter_select = self.box_value.get()
        filter_select=filter_select.replace(" ","")
        print(filter_select)
        self.show_frame(filter_select + "Page")

    #   OPEN FILE DIALOG TO UPLOAD IMAGE
    def fileInput(self):
        
        global idraw, upload_img
        self.filename1 = filedialog.askopenfilename(initialdir='/', title='Select A File',
                                                   filetypes=(("jpeg", "*.jpg"), ("All Files", "*.*")))
#         img_color = io.imread(self.filename)
#         img_gray = color.rgb2gray(img_color)
        img= cv2.imread(self.filename1,0)
#         img = Image.open(self.filename1)
#         img = img.resize((34, 26), Image.ANTIALIAS)
#         filter_class = BasicFilter.get_butterworth_low_pass_filter(img.shape, 75, 2)
#         output = filter_class.filtering()
#         output_dir = 'output/'
#         image_name = self.filename.split(".")
        # output_image_name = output_dir + image_name + datetime.now().strftime("%m%d-%H%M%S") + ".jpg"
#         output_image_name = output_dir + 'image.jpg'
#         img = img.resize(250, 250)
        img_resize=cv2.resize(img,(480,480))
        self.img_canvas_q2.image = ImageTk.PhotoImage(image=Image.fromarray(img_resize))
        self.img_canvas_q2.create_image(0, 0, image=self.img_canvas_q2.image, anchor='nw')

#         self.img_canvas_q1.image = ImageTk.PhotoImage(image=Image.fromarray(filter_class))
#         self.img_canvas_q1.create_image(0, 0, image=self.img_canvas_q1.image, anchor='nw')

    
    def filePara(self,filter_name,cutoff,order):
        
        self.frame_q4 = Frame(self, bg='#ffffff')
        self.frame_q4.place(relx=0, rely=.6, relwidth=0.3, relheight=1)
        
        self.frame_q5 = Frame(self, bg='#ffffff')
        self.frame_q5.place(relx=0.3, rely=.6, relwidth=1, relheight=1)
        
#         self.frame_q6 = Frame(self, bg='#ffffff')
#         self.frame_q6.place(relx=0.6, rely=1, relwidth=0.62, relheight=1)
        
        self.img_canvas_q3 = Canvas(self.frame_q5, bg='black')
        self.img_canvas_q3.place(relx=0, rely=0, relwidth=0.2, relheight=0.5)
    
        
        label1 = Label(self.frame_q4, text="Parameters chosen:", font=("Baskerville", 14), wraplength=300,padx=30,
                      justify=LEFT)
        label1.pack(side="top", fill="x", pady=10)
        
        label2 = Label(self.frame_q4, text="Filter: "+str(filter_name), font=("Baskerville", 14), wraplength=300,padx=30,
                          justify=LEFT)
        label2.pack(side="top", fill="x", pady=10)
        
        label3 = Label(self.frame_q4, text="Cutoff: "+str(cutoff), font=("Baskerville", 14), wraplength=300,padx=30,
                      justify=LEFT)
        label3.pack(side="top", fill="x", pady=10)
        
        label3 = Label(self.frame_q4, text="Order: "+str(order), font=("Baskerville", 14), wraplength=300,padx=30,
                  justify=LEFT)
        label3.pack(side="top", fill="x", pady=10)
        
        
        self.Evaluation(filter_name,cutoff,order)

    
    def fileOutput(self,filter_name,cutoff,order):
         
#         img_color = io.imread(self.filename)
#         img_gray = color.rgb2gray(img_color)

        img= cv2.imread(self.filename1,0)
        print(cutoff)
        if filter_name=="get_butterworth_high_pass_filter": 
            filter_class = BasicFilter.get_butterworth_high_pass_filter(img.shape, cutoff, order)
        elif filter_name=="get_butterworth_low_pass_filter": 
            filter_class = BasicFilter.get_butterworth_low_pass_filter(img.shape, cutoff, order)
        elif filter_name=="get_ideal_low_pass_filter": 
            filter_class = BasicFilter.get_ideal_low_pass_filter(img.shape, cutoff, order)
        elif filter_name=="get_ideal_high_pass_filter": 
            filter_class = BasicFilter.get_ideal_high_pass_filter(img.shape, cutoff, order)
        elif filter_name=="get_gaussian_low_pass_filter": 
            filter_class = BasicFilter.get_gaussian_low_pass_filter(img.shape, cutoff, order)
        elif filter_name=="get_gaussian_high_pass_filter": 
            filter_class = BasicFilter.get_gaussian_high_pass_filter(img.shape, cutoff, order)
        elif filter_name=="homomorphic_filter": 
            filter_class = BasicFilter.homo_filter(img, cutoff, order)
        else:
            label1 = Label(self.frame_q4, text="Filter not Found 🙅🏻‍♂️", font=("Baskerville", 14), wraplength=300,padx=30,
                      justify=LEFT)
            label1.pack(side="top", fill="x", pady=10)
            
        
        
                
#         output = filter_class.filtering()
#         output_dir = 'output/'
#         image_name = self.filename.split(".")
        # output_image_name = output_dir + image_name + datetime.now().strftime("%m%d-%H%M%S") + ".jpg"
#         output_image_name = output_dir + 'image.jpg'
#         self.img_canvas_q2.image = ImageTk.PhotoImage(image=Image.fromarray(img))
#         self.img_canvas_q2.create_image(0, 0, image=self.img_canvas_q2.image, anchor='nw')
        img_resize=cv2.resize(filter_class,(480,480))
        self.img_canvas_q1.image = ImageTk.PhotoImage(image=Image.fromarray(img_resize))
        self.img_canvas_q1.create_image(0, 0, image=self.img_canvas_q1.image, anchor='nw')
        
        self.filePara(filter_name,cutoff,order)
#         self.frame_q4.destroy()

        
    def fileOutput_o(self,filter_name,window_size):
        
        img= cv2.imread(self.filename1,0)
        print("in fileOutput_o")
        print("window_size: ",window_size)
        print("type window_size: ",type(window_size))
        if filter_name=="olympic": 
            filter_class = BasicFilter.olympic(img,window_size)
            
        self.img_canvas_q1.image = ImageTk.PhotoImage(image=Image.fromarray(filter_class))
        self.img_canvas_q1.create_image(0, 0, image=self.img_canvas_q1.image, anchor='nw')    
        
        self.filePara(filter_name,cutoff=75,order=2)
        
        self.Eval_O(filter_name=filter_name,cutoff=75,order=2,window_size=window_size)
    
    
    
    def Evaluation(self,filter_name,cutoff,order):
        
        img= cv2.imread(self.filename1,0)
        
        if filter_name== "get_butterworth_low_pass_filter" or filter_name=="get_gaussian_low_pass_filter" or filter_name=="get_ideal_low_pass_filter" or filter_name=="get_ideal_low_pass_filter" :
            
            no_1 = BasicFilter.get_gaussian_low_pass_filter(img.shape, cutoff, order)
            no_2 = BasicFilter.get_butterworth_low_pass_filter(img.shape, cutoff, order)
            no_3 = BasicFilter.get_ideal_low_pass_filter(img.shape, cutoff, order)
#             no_4 = BasicFilter.olympic(img,window_size)
            
            print("----------- EXECUTING-1 ------------")
            psnr1 = BasicFilter.PSNR(img,no_1)
            psnr2 = BasicFilter.PSNR(img,no_2)
            psnr3 = BasicFilter.PSNR(img,no_3)
#             psnr4 = BasicFilter.PSNR(img,no_4)
            
            
            print(psnr1)
            print(psnr2)
            print(psnr3)
#             print(psnr4)
            
            var = {psnr1:"psnr1",psnr2:"psnr2",psnr3:"psnr3"}
            var1 = max(var)
            print("MAX-PSNR: ",var1, max(var.get(max(var))))
            
            if var.get(max(var))=="psnr1":
                
                label1 = Label(self.frame_q4, text="SUGGESTED FILTER:\n   Gaussian Low Pass", font=("Baskerville", 16),fg="red", wraplength=300,padx=30,
                      justify=LEFT)
                label1.pack(side="top", fill="x", pady=10)
                
                no_1=cv2.resize(no_1,(300,300))
#             no_2=cv2.resize(no_2,(350,350))
#             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
        
                label2 = Label(self.frame_q4, text="* Low pass filters are compared only with other low pass filters", font=("Baskerville", 12),fg="blue", wraplength=300,padx=30,
                      justify=LEFT)
                label2.pack(side="top", fill="x", pady=10)
            
            if var.get(max(var))=="psnr2":
                
                label1 = Label(self.frame_q4, text="SUGGESTED FILTER:\n   Butterworth Low Pass", font=("Baskerville", 16),fg="red", wraplength=300,padx=30,
                      justify=LEFT)
                label1.pack(side="top", fill="x", pady=10)
                
                no_2=cv2.resize(no_2,(300,300))
#             no_2=cv2.resize(no_2,(350,350))
#             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_2))
                self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
        
                label2 = Label(self.frame_q4, text="* Low pass filters are compared only with other low pass filters", font=("Baskerville", 12),fg="blue", wraplength=300,padx=30,
                      justify=LEFT)
                label2.pack(side="top", fill="x", pady=10)
                
            if var.get(max(var))=="psnr3":
                
                label1 = Label(self.frame_q4, text="SUGGESTED FILTER:\n   Ideal Low Pass", font=("Baskerville", 16),fg="red", wraplength=300,padx=30,
                      justify=LEFT)
                label1.pack(side="top", fill="x", pady=10)
                
                label2 = Label(self.frame_q4, text="* Low pass filters are compared only with other low pass filters", font=("Baskerville", 12),fg="blue", wraplength=300,padx=30,
                      justify=LEFT)
                label2.pack(side="top", fill="x", pady=10)
                
                no_3=cv2.resize(no_3,(300,300))
#             no_2=cv2.resize(no_2,(350,350))
#             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_3))
                self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
        
#             if var.get(max(var))=="psnr4":
                
#                 label1 = Label(self.frame_q4, text="SUGGESTED FILTER:\n Olympic", font=("Baskerville", 16),fg="red", wraplength=300,padx=30,
#                       justify=LEFT)
#                 label1.pack(side="top", fill="x", pady=10)
                
#                 label2 = Label(self.frame_q4, text="* Low pass filters are compared only with other low pass filters", font=("Baskerville", 12),fg="blue", wraplength=300,padx=30,
#                       justify=LEFT)
#                 label2.pack(side="top", fill="x", pady=10)
                
#                 no_4=cv2.resize(no_4,(300,300))
# #             no_2=cv2.resize(no_2,(350,350))
# #             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
#                 self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_4))
#                 self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
            
        elif filter_name== "get_butterworth_high_pass_filter" or filter_name=="get_gaussian_high_pass_filter" or filter_name=="get_ideal_high_pass_filter" or filter_name=="homomorphic_filter":
            
            no_1 = BasicFilter.get_gaussian_high_pass_filter(img.shape, cutoff, order)
            no_2 = BasicFilter.get_butterworth_high_pass_filter(img.shape, cutoff, order)
            no_3 = BasicFilter.get_ideal_high_pass_filter(img.shape, cutoff, order)
            no_4 = BasicFilter.homo_filter(img, cutoff, order)
            
            psnr1 = BasicFilter.PSNR(img,no_1)
            psnr2 = BasicFilter.PSNR(img,no_2)
            psnr3 = BasicFilter.PSNR(img,no_3)
            psnr4 = BasicFilter.PSNR(img,no_4)
            
            print("----------- EXECUTING-2 ------------")
            print(psnr1)
            print(psnr2)
            print(psnr3)
            print(psnr4)
            
#             M_Psnr= max[psnr1,psnr2,psnr3,psnr4]
#             print("Max_PSNR: ",M_Psnr)
            
            var = {psnr1:"psnr1",psnr2:"psnr2",psnr3:"psnr3",psnr4:"psnr4"}
            var1 = max(var)
            print("MAX-PSNR: ",var1, var.get(max(var)))
            
            if var.get(max(var))=="psnr1":
                
                label1 = Label(self.frame_q4, text="SUGGESTED FILTER:\nGaussian High Pass", font=("Baskerville", 16),fg="red", wraplength=300,padx=30,
                      justify=LEFT)
                label1.pack(side="top", fill="x", pady=10)
                
                no_1=cv2.resize(no_1,(300,300))
#             no_2=cv2.resize(no_2,(350,350))
#             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
        
                label2 = Label(self.frame_q4, text="* High pass filters are compared only with other High pass filters", font=("Baskerville", 12),fg="blue", wraplength=300,padx=30,
                      justify=LEFT)
                label2.pack(side="top", fill="x", pady=10)
            
            if var.get(max(var))=="psnr2":
                
                label1 = Label(self.frame_q4, text="SUGGESTED FILTER:\nButterworth High Pass", font=("Baskerville", 16),fg="red", wraplength=300,padx=30,
                      justify=LEFT)
                label1.pack(side="top", fill="x", pady=10)
                
                no_2=cv2.resize(no_2,(300,300))
#             no_2=cv2.resize(no_2,(350,350))
#             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_2))
                self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
        
                label2 = Label(self.frame_q4, text="* High pass filters are compared only with other High pass filters", font=("Baskerville", 12),fg="blue", wraplength=300,padx=30,
                      justify=LEFT)
                label2.pack(side="top", fill="x", pady=10)
                
            if var.get(max(var))=="psnr3":
                
                label1 = Label(self.frame_q4, text="SUGGESTED FILTER:\nIdeal High Pass", font=("Baskerville", 16),fg="red", wraplength=300,padx=30,
                      justify=LEFT)
                label1.pack(side="top", fill="x", pady=10)
                
                no_3=cv2.resize(no_3,(300,300))
#             no_2=cv2.resize(no_2,(350,350))
#             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_3))
                self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
        
                label2 = Label(self.frame_q4, text="* High pass filters are compared only with other High pass filters", font=("Baskerville", 12),fg="blue", wraplength=300,padx=30,
                      justify=LEFT)
                label2.pack(side="top", fill="x", pady=10)
                
            if var.get(max(var))=="psnr4":
                
                label1 = Label(self.frame_q4, text="SUGGESTED FILTER:\nHomomorphic Pass", font=("Baskerville", 16),fg="red", wraplength=300,padx=30,
                      justify=LEFT)
                label1.pack(side="top", fill="x", pady=10)
                no_4=cv2.resize(no_4,(300,300))
#             no_2=cv2.resize(no_2,(350,350))
#             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_4))
                self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
                
                label2 = Label(self.frame_q4, text="* High pass filters are compared only with other High pass filters", font=("Baskerville", 12),fg="blue", wraplength=300,padx=30,
                      justify=LEFT)
                label2.pack(side="top", fill="x", pady=10)
                
            
            
#             no_1=cv2.resize(no_1,(300,300))
# #             no_2=cv2.resize(no_2,(350,350))
# #             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
#             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
#             self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
# #         label = Label(self, text="PNSR Values", font=self.controller.fontSize, wraplength=30,
# #                       justify=RIGHT)
# #         label.pack(side="bottom",  pady=100)
            
    def Eval_O(self,filter_name,cutoff,order,window_size):
        
        img= cv2.imread(self.filename1,0)
        
        if filter_name== "olympic":
            
            no_1 = BasicFilter.get_gaussian_low_pass_filter(img.shape, cutoff, order)
            no_2 = BasicFilter.get_butterworth_low_pass_filter(img.shape, cutoff, order)
            no_3 = BasicFilter.get_ideal_low_pass_filter(img.shape, cutoff, order)
            no_4 = BasicFilter.olympic(img,window_size)
            
            print("----------- EXECUTING-1 ------------")
            psnr1 = BasicFilter.PSNR(img,no_1)
            psnr2 = BasicFilter.PSNR(img,no_2)
            psnr3 = BasicFilter.PSNR(img,no_3)
            psnr4 = BasicFilter.PSNR(img,no_4)
            
            
            print(psnr1)
            print(psnr2)
            print(psnr3)
            print(psnr4)
            
            var = {psnr1:"psnr1",psnr2:"psnr2",psnr3:"psnr3",psnr4:"psnr4"}
            var1 = max(var)
            print("MAX-PSNR: ",var1, max(var.get(max(var))))
            
            if var.get(max(var))=="psnr1":
                
                label1 = Label(self.frame_q4, text="SUGGESTED FILTER:\n   Gaussian Low Pass", font=("Baskerville", 16),fg="red", wraplength=300,padx=30,
                      justify=LEFT)
                label1.pack(side="top", fill="x", pady=10)
                
                no_1=cv2.resize(no_1,(300,300))
#             no_2=cv2.resize(no_2,(350,350))
#             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
        
                label2 = Label(self.frame_q4, text="* Low pass filters are compared only with other low pass filters", font=("Baskerville", 12),fg="blue", wraplength=300,padx=30,
                      justify=LEFT)
                label2.pack(side="top", fill="x", pady=10)
            
            if var.get(max(var))=="psnr2":
                
                label1 = Label(self.frame_q4, text="SUGGESTED FILTER:\n   Butterworth Low Pass", font=("Baskerville", 16),fg="red", wraplength=300,padx=30,
                      justify=LEFT)
                label1.pack(side="top", fill="x", pady=10)
                
                no_2=cv2.resize(no_2,(300,300))
#             no_2=cv2.resize(no_2,(350,350))
#             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_2))
                self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
        
                label2 = Label(self.frame_q4, text="* Low pass filters are compared only with other low pass filters", font=("Baskerville", 12),fg="blue", wraplength=300,padx=30,
                      justify=LEFT)
                label2.pack(side="top", fill="x", pady=10)
                
            if var.get(max(var))=="psnr3":
                
                label1 = Label(self.frame_q4, text="SUGGESTED FILTER:\n   Ideal Low Pass", font=("Baskerville", 16),fg="red", wraplength=300,padx=30,
                      justify=LEFT)
                label1.pack(side="top", fill="x", pady=10)
                
                label2 = Label(self.frame_q4, text="* Low pass filters are compared only with other low pass filters", font=("Baskerville", 12),fg="blue", wraplength=300,padx=30,
                      justify=LEFT)
                label2.pack(side="top", fill="x", pady=10)
                
                no_3=cv2.resize(no_3,(300,300))
#             no_2=cv2.resize(no_2,(350,350))
#             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_3))
                self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
        
            if var.get(max(var))=="psnr4":
                
                label1 = Label(self.frame_q4, text="SUGGESTED FILTER:\n   Ideal Low Pass", font=("Baskerville", 16),fg="red", wraplength=300,padx=30,
                      justify=LEFT)
                label1.pack(side="top", fill="x", pady=10)
                
                label2 = Label(self.frame_q4, text="* Low pass filters are compared only with other low pass filters", font=("Baskerville", 12),fg="blue", wraplength=300,padx=30,
                      justify=LEFT)
                label2.pack(side="top", fill="x", pady=10)
                
                no_4=cv2.resize(no_4,(300,300))
#             no_2=cv2.resize(no_2,(350,350))
#             self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_1))
                self.img_canvas_q3.image = ImageTk.PhotoImage(image=Image.fromarray(no_4))
                self.img_canvas_q3.create_image(0, 0, image=self.img_canvas_q3.image, anchor='nw')
            
        

#   PAGE IN MIDDLE FRAME

class FirstPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label1 = Label(self, text="FREQUENCY FILTERING\n", font=("Apple Chancery", 18), wraplength=300,padx=30,
                      justify=LEFT)
        label1.pack(side="top", fill="x", pady=10)
        label2 = Label(self, text="1.Please upload the picture \n 2.Choose the filter \n 3.click on apply", font=("Helvetica", 16), wraplength=300,
                      justify=LEFT)
        label2.pack(side="top", fill="x", pady=10)
        
class ButterworthHighPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Butterworth High Filter Options", font=self.controller.fontSize, wraplength=200,
                      justify=LEFT)
        label.pack(side="top", fill="x", pady=10)
        
        label = tk.Label(self, text="Choose the cutoff: ", font=LARGE_FONT)
        label.pack(pady=40,padx=40)
        
        cutoff_slider = Scale(self, from_=50, to=150, orient=HORIZONTAL)
        cutoff_slider.set(19)
        cutoff_slider.pack()
        
        label = tk.Label(self, text="Choose the order: ", font=LARGE_FONT)
        label.pack(pady=40,padx=40)
        
        order_slider = Scale(self, from_=0, to=10, orient=HORIZONTAL)
        order_slider.set(5)
        order_slider.pack()
        
        button = Button(self, text="SUBMIT",
                        command=lambda: app.fileOutput(filter_name="get_butterworth_high_pass_filter",cutoff=cutoff_slider.get(),order=order_slider.get()) )
        button.pack()

class ButterworthLowPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Butterworth Low Filter Options", font=self.controller.fontSize, wraplength=200,
                      justify=LEFT)
        label.pack(side="top", fill="x", pady=10)
        
        label = tk.Label(self, text="Choose the cutoff: ", font=LARGE_FONT)
        label.pack(pady=40,padx=40)
        
        cutoff_slider = Scale(self, from_=50, to=150, orient=HORIZONTAL)
        cutoff_slider.set(19)
        cutoff_slider.pack()
        
        label = tk.Label(self, text="Choose the order: ", font=LARGE_FONT)
        label.pack(pady=40,padx=40)
        
        order_slider = Scale(self, from_=0, to=10, orient=HORIZONTAL)
        order_slider.set(5)
        order_slider.pack()
        
        button = Button(self, text="SUBMIT",
                        command=lambda: app.fileOutput(filter_name="get_butterworth_low_pass_filter",cutoff=cutoff_slider.get(),order=order_slider.get()) )
        button.pack()
        
        


# PAGE IN MIDDLE FRAME
class GaussianHighPage(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Gaussian High Filter Options", font=controller.fontSize, wraplength=200,
                      justify=LEFT)
        label.pack(side="top", fill="x", pady=10)
        
        label = tk.Label(self, text="Choose the Cutoff Frequency: ", font=LARGE_FONT)
        label.pack(pady=20,padx=20)
        
        cutoff_slider = Scale(self, from_=50, to=150, orient=HORIZONTAL)
        cutoff_slider.set(19)
        cutoff_slider.pack()
#         print(app.filename1)
        
#       img=cv2.imread("/Users/shreyas/Downloads/Lenna0.jpg",0)
#         print(img.shape)
#        s=Application()
        button = Button(self, text="SUBMIT",
                        command=lambda: app.fileOutput(filter_name="get_gaussian_high_pass_filter",cutoff=cutoff_slider.get(),order=2) )
        button.pack()
        
        
class GaussianLowPage(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Gaussian Low Filter Options", font=controller.fontSize, wraplength=200,
                      justify=LEFT)
#         img=cv2.imread("/Users/shreyas/Downloads/Lenna0.jpg",0)
#         print(img.shape)
        label.pack(side="top", fill="x", pady=10)
    
        label = tk.Label(self, text="Choose the Cutoff Frequency: ", font=LARGE_FONT)
        label.pack(pady=20,padx=20)
        
        cutoff_slider = Scale(self, from_=50, to=150, orient=HORIZONTAL)
        cutoff_slider.set(19)
        cutoff_slider.pack()
        button = Button(self, text="SUBMIT",
                        command=lambda: app.fileOutput(filter_name="get_gaussian_low_pass_filter",cutoff=cutoff_slider.get(),order=2) )
        button.pack()


#   PAGE IN MIDDLE FRAME
class OlympicPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        btn = IntVar()

        label = Label(self, text="Olympic Filter Options", font=controller.fontSize, wraplength=200,
                      justify=LEFT)
        label.grid(row=1, column=1, sticky='n')
        
      
        b1 = Radiobutton(self,
                text = "3",
                value = 3,variable=btn)
        b1.grid()
        
        b2 = Radiobutton(self,
                text = "5",
                value = 5, variable= btn)
        b2.grid()
        
        button = Button(self, text="SUBMIT",
                        command=lambda: app.fileOutput_o(filter_name="olympic",window_size=btn.get()) )
        button.grid()
        
        print(X)


#   PAGE IN MIDDLE FRAME
class HomomorphicPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Homomorphic Filter Options", font=controller.fontSize, wraplength=200,
                      justify=LEFT)
        label.pack(side="top", fill="x", pady=10)
        
        label = tk.Label(self, text="Choose the Cutoff Frequency: ", font=LARGE_FONT)
        label.pack(pady=20,padx=20)
        
        cutoff_slider = Scale(self, from_=50, to=150, orient=HORIZONTAL)
        cutoff_slider.set(19)
        cutoff_slider.pack()
        
        label = tk.Label(self, text="Choose the order: ", font=LARGE_FONT)
        label.pack(pady=40,padx=40)
        
        order_slider = Scale(self, from_=0, to=10, orient=HORIZONTAL)
        order_slider.set(5)
        order_slider.pack()
        
        button = Button(self, text="SUBMIT",
                        command=lambda: app.fileOutput(filter_name="homomorphic_filter",cutoff=cutoff_slider.get(),order=order_slider.get()) )
        button.pack()


#   PAGE IN MIDDLE FRAME
class IdealHighPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Ideal High Filter Options", font=controller.fontSize, wraplength=200,
                      justify=LEFT)
        label.pack(side="top", fill="x", pady=10)
        
        label = tk.Label(self, text="Choose the Cutoff Frequency: ", font=LARGE_FONT)
        label.pack(pady=20,padx=20)
        
        cutoff_slider = Scale(self, from_=50, to=150, orient=HORIZONTAL)
        cutoff_slider.set(19)
        cutoff_slider.pack()
        
#         label = tk.Label(self, text="Choose the order: ", font=LARGE_FONT)
#         label.pack(pady=40,padx=40)
        
#         order_slider = Scale(self, from_=0, to=10, orient=HORIZONTAL)
#         order_slider.set(5)
#         order_slider.pack()
        
        button = Button(self, text="SUBMIT",
                        command=lambda: app.fileOutput(filter_name="get_ideal_high_pass_filter",cutoff=cutoff_slider.get(),order=2) )
        button.pack()
        
class IdealLowPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Ideal Low Filter Options", font=controller.fontSize, wraplength=200,
                      justify=LEFT)
        label.pack(side="top", fill="x", pady=10)
        
        label = tk.Label(self, text="Choose the Cutoff Frequency: ", font=LARGE_FONT)
        label.pack(pady=20,padx=20)

        cutoff_slider = Scale(self, from_=50, to=150, orient=HORIZONTAL)
        cutoff_slider.set(19)
        cutoff_slider.pack()
        
#         label = tk.Label(self, text="Choose the order: ", font=LARGE_FONT)
#         label.pack(pady=40,padx=40)
        
#         order_slider = Scale(self, from_=0, to=10, orient=HORIZONTAL)
#         order_slider.set(5)
#         order_slider.pack()
        
        button = Button(self, text="SUBMIT",
                        command=lambda: app.fileOutput(filter_name="get_ideal_low_pass_filter",cutoff=cutoff_slider.get(),order=2) )
        button.pack()
        
        



if __name__ == '__main__':
    app = Application()
    app.mainloop()




