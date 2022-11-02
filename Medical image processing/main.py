from ast import Pass
import tkinter as tk
import tkinter.scrolledtext as tkst
from collections import deque
from tkinter import filedialog
from tkinter import messagebox as mBox
from tkinter import ttk
from turtle import color
import cv2
import matplotlib.cm as cm
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import sklearn.metrics as sm
from matplotlib import cm, path
from matplotlib import pyplot as plt
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.image import imread
from matplotlib.path import Path
from matplotlib.widgets import LassoSelector, Slider
from PIL import Image, ImageTk
from pylab import *
from scipy import ndimage as ndi
from skimage import data
from skimage.feature import canny, peak_local_max
from skimage.segmentation import watershed
from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from sklearn.cluster import KMeans



############## main windows ############
window = tk.Tk()
window.geometry('1500x1500')

########################## Open file ##################################
def OPEN():
    global Original_Image
    global Dimension_Number
    global Original_image_Size
    window.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                filetypes=(("png files", "*.png"),("jpeg files", "*.jpg"),("tif files", "*.TIF"), ("all files", "*.*")))
    Original_Image = Image.open(window.filename)
    Original_Image=np.array(Original_Image)
    Original_image_Size = np.shape(Original_Image)
    print(len(Original_image_Size))

    a1 = np.shape(Original_Image)
    a1 = str(a1)
  
    
    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("channel ", x1 + 1))


  
        
    def RGB_Showcus():

        image_name = window.filename.split("/")[-1]   
        tk.Label(master=window, text=image_name, bg="#007AA8", fg="white",
                     font=("times new roman", 20, "bold")).place(x=0, y=150)
        image = Original_Image
        image = Image.fromarray(image)
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(window,image=photo)
        label.place(x=370, y=130)

        window.mainloop()   

    

    


    RGB_btn = tk.Button(window, bg='#0e3a53', fg='#aaf0c1', text='   Show image   ' , font=("times new roman", 15, "bold"), padx=60, bd='5', command=RGB_Showcus)
    RGB_btn.place(x=540,y=630)
   
    
   
########################## Histogram ##################################

def Show_Histogram1():
    root4 = tk.Toplevel()
    root4.geometry("900x900")
    root4.configure(background='white')
    root4.title("Traitement des imageries médicales")

    frame1 = tk.Frame(
        master=root4,
        bg='#808000'
    )
    frame1.place(x=0, y=200)
   
    def Show_Histogram2():
        
        # show histogram of the channel correspond to the Number 
    
        if len(Original_image_Size) > 2:
            a_Histogram = int(numberChosen1.get())
            img = Original_Image[:, :, a_Histogram - 1]
            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])

            fig = plt.Figure(figsize=(10, 6),facecolor='white')

            canvas = FigureCanvasTkAgg(fig, root4)
            canvas.get_tk_widget().place(x=100, y=50)

            toolbarFrame = tk.Frame(master=root4)
            toolbarFrame.place(x=520,y=600)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            
            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");
            ax2.set_facecolor(color="#aaf0c1")

            fig.subplots_adjust(bottom=0.25)
            
            ax1.imshow(img, cmap='gray')            
            ax2.plot(range(256), hist_img.ravel(),color="#0e3a53",label="channel"+str(a_Histogram))

            ax2.set_title("channel" + str(a_Histogram) + " Histogram", fontsize=12, color="#333533")

            ax1.legend(loc='best')
            ax2.legend(loc='best')


            fig.canvas.draw_idle()


    def gray_img():        
        # show histogram of the gray channel  
    
        img = cv2.cvtColor(Original_Image,cv2.COLOR_BGR2GRAY)
        hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])

        fig = plt.Figure(figsize=(10, 6),facecolor='white')

        canvas = FigureCanvasTkAgg(fig, root4)
        canvas.get_tk_widget().place(x=100, y=50)

        toolbarFrame = tk.Frame(master=root4)
        toolbarFrame.place(x=520,y=600)

        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect("key_press_event", on_key_press)

        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        ax1.set_title("Original Image", fontsize=12, color="#333533")
        
        ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
        ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

        ax2.set_facecolor(color="#aaf0c1")

        fig.subplots_adjust(bottom=0.25)
        
        ax1.imshow(img, cmap='gray')            

        ax2.plot(range(256), hist_img.ravel(),color="#0e3a53",label="gray scale")

        ax2.set_title("Histogram for gray scale image", fontsize=12, color="#333533")

        ax1.legend(loc='best')
        ax2.legend(loc='best')

        fig.canvas.draw_idle()

  

  
        
    def ALL_channelS():

        color = ('b', 'g', 'r')
        fig = plt.Figure(figsize=(10, 6),facecolor='white')

        canvas = FigureCanvasTkAgg(fig, root4)
        canvas.get_tk_widget().place(x=100, y=50)

        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        
        ax1.set_title("Original Image", fontsize=12, color="#333533")

        ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
        ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

        ax2.set_facecolor("#aaf0c1")

        toolbarFrame = tk.Frame(master=root4)
        toolbarFrame.place(x=520, y=600)

        ax2.set_title("Histogram")
        ax1.imshow(Original_Image, cmap='gray')            

        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect("key_press_event", on_key_press)

        fig.subplots_adjust(bottom=0.25)
        k=0
        for i, col in enumerate(color):
            k=1+k
            hist_RGB = cv2.calcHist([Original_Image], [i], None, [256], [0, 256])
            ax2.plot(range(256), hist_RGB.ravel(), color=col,label="channel"+str(k))

            ax1.legend(loc='best')
            ax2.legend(loc='best')

            fig.canvas.draw_idle()
    if len(Original_image_Size) > 2:

        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("channel ", x1 + 1))

    if len(Original_image_Size) > 2:
        ttk.Label(root4, text="Choose a channel:",font=('Franklin Gothic Demi Cond', 11)).place(x=0,y=0)
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root4, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.place(x=150,y=0)
        numberChosen1.current(0)
        if Original_image_Size[2] == 3:
            RGB_btn = tk.Button(root4, bg='#0e3a53', fg='#aaf0c1', text='   One Channel  ', padx=40, bd='10',
                                command=Show_Histogram2)
            RGB_btn.place(x=320, y=0)
            
            RGB_btn1 = tk.Button(root4, bg='#0e3a53', fg='#aaf0c1', text='   All channels   ', padx=40, bd='10',
                                 command=ALL_channelS)
            RGB_btn1.place(x=520, y=0)
            
            RGB_btn2 = tk.Button(root4, bg='#0e3a53', fg='#aaf0c1', text='   Grayscale   ', padx=40, bd='10',
                                 command=gray_img)
            RGB_btn2.place(x=720, y=0)
            
            

        def Quit():
           root4.quit()
           root4.destroy()

        button = tk.Button(master=root4, bg='#0e3a53', fg='#aaf0c1', text='       Quit        ', padx=40,
                            bd='10', command=Quit)
        button.place(x=920, y=0)


    root4.mainloop()

    
    
####################################### Filtering ##########################################
    

    
######################################Averaging Filter######################################


def AverageFilter():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("Traitement des imageries médicales")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')


    def AveragingFilter1():
        if len(Original_image_Size) > 2:
            a_AverageFiltering = int(numberChosen1.get())
            img = Original_Image[:, :, a_AverageFiltering - 1]
            fig = plt.Figure(figsize=(10, 6),facecolor='white')

            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=100, y=50)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_title("Histogram", fontsize=12, color="#333533")

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#aaf0c1")

            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=520, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def AverageFiltering2():
                ax2.cla()
                E11 = int(E1.get())
                E22 = int(E2.get())
                kernel_3 = np.ones((E11, E22), np.float32) / (E11 * E22)

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(),color="#0e3a53", label="channel" + str(a_AverageFiltering)+"Histogram")
                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(),color="coral", label="Filtered Image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");
                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax2.legend(loc='best')


                fig.canvas.draw_idle()

            L1 = tk.Label(root8, text="Row:", bg='#0e3a53', fg='#aaf0c1', bd=5)
            L1.place(x=350, y=600)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=380, y=600)

            L2 = tk.Label(root8, text="Column:", bg='#0e3a53', fg='#aaf0c1', bd=5)
            L2.place(x=520, y=600)
            E2 = tk.Entry(root8, bd=5)
            E2.place(x=570, y=600)
            btn2 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   Apply   ', padx=20, bd='1',
                             command=AverageFiltering2)
            btn2.place(x=680, y=600)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="#0e3a53", label="channel" + str(a_AverageFiltering)+"Histogram")
            ax2.legend(loc='best')
            fig.canvas.draw_idle()

            

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("channel", x1 + 1))

    
    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a channel:", font=('Franklin Gothic Demi Cond', 11)).place(x=0,y=0)
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.place(x=150,y=0)
        numberChosen1.current(0)
        if len(Original_image_Size) == 3:
            def RGBAvrageFil():
                img = Original_Image
                fig = plt.Figure(figsize=(10, 6),facecolor='white')

                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=100, y=50)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_title("Histogram", fontsize=12, color="#333533")

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#aaf0c1")

                ax1.set_title("Original Image", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=520, y=650)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                def AverageFiltering2():
                    ax2.cla()
                    E11 = int(E1.get())
                    E22 = int(E2.get())
                    kernel_3 = np.ones((E11, E22), np.float32) / (E11 * E22)

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')

                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                    ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                    ax2.set_facecolor("#aaf0c1")

                    ax1.set_title("Filtred Image", fontsize=12, color="#333533")

                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="channel" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="channel" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="channel" + str(3) + "Histogram")


                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="#0e3a53", label= "Filtered Image Histogram")
                    ax2.legend(loc='best')


                    fig.canvas.draw_idle()

                L1 = tk.Label(root8, text="Row:", bg='#0e3a53', fg='#aaf0c1', bd=5)
                L1.place(x=350, y=600)
                E1 = tk.Entry(root8, bd=5)
                E1.place(x=380, y=600)

                L2 = tk.Label(root8, text="Column:", bg='#0e3a53', fg='#aaf0c1', bd=5)
                L2.place(x=520, y=600)
                E2 = tk.Entry(root8, bd=5)
                E2.place(x=570, y=600)
                btn2 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   Apply   ', padx=20, bd='1',
                                 command=AverageFiltering2)
                btn2.place(x=680, y=600)

                hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img0.ravel(), color="r", label="channel" + str(1) + "Histogram")
                hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                ax2.plot(range(256), hist_img1.ravel(), color="g", label="channel" + str(2) + "Histogram")
                hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                ax2.plot(range(256), hist_img2.ravel(), color="b", label="channel" + str(3) + "Histogram")
                ax2.legend(loc='best')

        btn11 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   One channel  ', padx=40, bd='10',
                            command=AveragingFilter1)
        btn11.place(x=320, y=0)
        
        
        btn12 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   All channels  ', padx=40, bd='10',
                        command=RGBAvrageFil)
        btn12.place(x=520, y=0)
        
        btn11 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   Grayscale  ', padx=40, bd='10',
                            command=AveragingFilter1)
        btn11.place(x=720, y=0)



    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#0e3a53', fg='#aaf0c1', text='       Quit        ', padx=40,
                       bd='10', command=Quit)
    button.place(x=920,y=0)

    root8.mainloop()

    

    
###################################### Median Filter ######################################


def MedianFilter():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("TP imagerie mediacale Sup'Com")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')


    def MedianFilter1():
        if len(Original_image_Size) > 2:
            a_AverageFiltering = int(numberChosen1.get())
            img = Original_Image[:, :, a_AverageFiltering - 1]
            fig = plt.Figure(figsize=(10, 6),facecolor='white')

            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=100, y=50)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_title("Histogram", fontsize=12, color="#333533")

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#aaf0c1")

            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=850, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def MedianFilter2():
                ax2.cla()
                E11 = int(E1.get())

                q = cv2.medianBlur(img, E11)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="#0e3a53", label="channel"+str(a_AverageFiltering)+"Histogram")
                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="coral", label="Filtered Image Histogram")

                ax2.set_title("Histogram", fontsize=12, color="#333533")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            L1 = tk.Label(root8, text="Kernel Size(Odd Number):", bg='#0e3a53', fg='#aaf0c1', bd=5)
            L1.place(x=400, y=650)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=550, y=650)

            btn2 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   Apply   ', padx=20, bd='1',
                             command=MedianFilter2)
            btn2.place(x=680, y=650)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="#0e3a53", label="channel"+str(a_AverageFiltering)+"Histogram")
            ax2.legend(loc='best')
            fig.canvas.draw_idle()

       

            L1 = tk.Label(root8, text="Kernel Size(Odd Number):", bg='#0e3a53', fg='#aaf0c1', bd=5)
            L1.place(x=400, y=650)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=550, y=650)

            btn2 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   Apply   ', padx=20, bd='1',
                             command=MedianFilter2)
            btn2.place(x=680, y=650)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="#0e3a53", label="channel" + str(1) + "Histogram")
            ax2.legend(loc='best')
            fig.canvas.draw_idle()

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("channel", x1 + 1))

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a channel:", font=('Franklin Gothic Demi Cond', 11)).place(x=0,y=0)
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.place(x=150,y=0)
        numberChosen1.current(0)
        if len(Original_image_Size) == 3:
            def RGBMedianFil():
                img = Original_Image
                fig = plt.Figure(figsize=(10, 6),facecolor='white')

                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=100, y=50)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_title("Histogram", fontsize=12, color="#333533")

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#aaf0c1")

                ax1.set_title("Original Image", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=850, y=650)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)


                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                def MedianFilter2():
                    ax2.cla()
                    E11 = int(E1.get())

                    q = cv2.medianBlur(img, E11)
                    ax1.imshow(q, cmap='gray')

                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel() ,color="r", label="channel1 Histogram")

                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="channel2 Histogram")

                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="channel3 Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="#0e3a53", label="Filtered Image Histogram")
                    ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                L1 = tk.Label(root8, text="Kernel Size(Odd Number):", bg='#0e3a53', fg='#aaf0c1', bd=5)
                L1.place(x=400, y=650)
                E1 = tk.Entry(root8, bd=5)
                E1.place(x=550, y=650)

                btn2 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   Apply   ', padx=20, bd='1',
                                 command=MedianFilter2)
                btn2.place(x=680, y=650)

                hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img0.ravel(), color="r", label="channel1 Histogram")

                hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                ax2.plot(range(256), hist_img1.ravel(), color="g", label="channel2 Histogram")

                hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                ax2.plot(range(256), hist_img2.ravel(), color="b", label="channel3 Histogram")
                ax2.legend(loc='best')


        btn23 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   All channel  ', padx=40, bd='10',
                            command=RGBMedianFil)
        btn23.place(x=520,y=0)
        btn24 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   One channel  ', padx=40, bd='10',
                        command=MedianFilter1)
        btn24.place(x=320,y=0)
        
        btn24 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   Grayscale  ', padx=40, bd='10',
                        command=MedianFilter1)
        btn24.place(x=720,y=0)



    def Quit():
        root8.quit()
        root8.destroy()

    button11 = tk.Button(master=root8, bg='#0e3a53', fg='#aaf0c1', text='       Quit        ', padx=40,
                       bd='10', command=Quit)
    button11.place(x=920,y=0)

    root8.mainloop()

###################################### Segmentation ######################################

    
###################################### Edge Detection ######################################


def Canny():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("TP Traitement des imageries médicales")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
   
    def Canny1():
        if len(Original_image_Size) > 2:
            a_Canny = int(numberChosen1.get())
            img = Original_Image[:, :, a_Canny - 1]
            fig = plt.Figure(figsize=(10, 6),facecolor='white')

            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=100, y=40)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)



            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#aaf0c1")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=600, y=630)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)


            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

            s_time1 = Slider(ax1_value, 'Minimum Value', 0, np.max(img), valinit=0, color='r')
            s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')




            def Canny2(val):
                ax2.cla()
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(),color="#aaf0c1",label="Channel"+str(a_Canny)+"Histogram")

                ax2.axvline(x=int(s_time1.val), color='r',label="Minimum")
                ax2.axvline(x=int(s_time2.val), color='g',label="Maximum")

                ax2.legend(loc='best')

                q = cv2.Canny(img, int(s_time1.val), int(s_time2.val))
                ax1.imshow(q, cmap='gray')





                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Segmented Image", fontsize=12, color="#333533")

                fig.canvas.draw_idle()

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(),color="#aaf0c1",label="Channel"+str(a_Canny)+"Histogram")

            ax2.legend(loc='best')

        
            
            s_time1.on_changed(Canny2)
            s_time2.on_changed(Canny2)


    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Channel ", x1 + 1))

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a channel:", font=('Franklin Gothic Demi Cond', 11)).place(x=0,y=0)
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.place(x=150,y=0)
        numberChosen1.current(0)

        btn25 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   One channel   ', padx=40, bd='10',
                        command=Canny1)
        btn25.place(x=320,y=0)

        
        btn26 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   Grayscale   ', padx=40, bd='10',
                        command=Canny1)
        btn26.place(x=520,y=0)

    def Quit():
        root8.quit()
        root8.destroy()

    button3 = tk.Button(master=root8, bg='#0e3a53', fg='#aaf0c1', text='       Quit        ', padx=40,
                       bd='10', command=Quit)
    button3.place(x=720,y=0)

    root8.mainloop()

###################################### thresholding ######################################

###################################### Simple thresholding ######################################
    
def thresholding():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("TP Traitement des imageries médicales")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
   


    def thresholding1():
        if len(Original_image_Size) > 2:
            global imgT
            a_thresholding = int(numberChosen1.get())
            imgT = Original_Image[:, :, a_thresholding - 1]

            fig = plt.Figure(figsize=(10, 6),facecolor='white')

            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=100, y=50)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)


            ax2.set_title(" Histogram", fontsize=12, color="#333533")

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#aaf0c1")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(imgT, cmap='gray')

            hist_img = cv2.calcHist([imgT], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(),color="#0e3a53",label="Channel"+str(a_thresholding)+"Histogram")



            ax2.axvline(x=0,label="threshold", color='r')
            ax2.legend(loc='best')


            fig.canvas.draw_idle()

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time = Slider(ax1_value, 'thresholding:', 0, 255, valinit=0,color='r')

            def update(val):
                ax2.cla()

                hist_img = cv2.calcHist([imgT], [0], None, [256], [0, 256])
                a_thresholding = int(numberChosen1.get())
                ax2.bar(range(256), hist_img.ravel(),color="#0e3a53",label="Channel"+str(a_thresholding)+"Histogram")
                ax2.axvline(x=int(s_time.val),label="threshold", color='r')


                img = Original_Image[:, :, a_thresholding - 1]
                img = np.array(img)
                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        if img[i, j] > s_time.val:
                            img[i, j] = 255
                        else:
                            img[i, j] = 0
                img3 = img
                ax1.imshow(img3, cmap='gray')

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("thresholding Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax2.legend(loc='best')


                fig.canvas.draw_idle()

            s_time.on_changed(update)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Channel ", x1 + 1))

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a channel:", font=('Franklin Gothic Demi Cond', 11)).place(x=0,y=0)
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.place(x=150,y=0)
        numberChosen1.current(0)

        btn25 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   One channel   ', padx=40, bd='10',
                        command=thresholding1)
        btn25.place(x=320,y=0)

        
        btn26 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   Grayscale   ', padx=40, bd='10',
                        command=thresholding1)
        btn26.place(x=520,y=0)

    def Quit():
        root8.quit()
        root8.destroy()

    button3 = tk.Button(master=root8, bg='#0e3a53', fg='#aaf0c1', text='       Quit        ', padx=40,
                       bd='10', command=Quit)
    button3.place(x=720,y=0)

    root8.mainloop()


    
############################### Segmentation by regions #####################

    
###################################### Kmeans ######################################


def Kmeans_seg():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("TP Traitement des imageries médicales")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    
    def Kmeans_seg1():
        if len(Original_image_Size) > 2:

            a_Dilation = int(numberChosen1.get())
            img = Original_Image[:, :, a_Dilation - 1]
            img=img/255.0
            vectorized = img.reshape((-1,1)) 
            vectorized = np.float32(vectorized)
            fig = plt.Figure(figsize=(10, 6),facecolor='white')

            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=100, y=50)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Kmeans_seg2():
                root9 = tk.Tk()

                root9.configure(background='white')
                root9.title("TP Traitement des imageries médicales")
                ax2.cla()
                height = int(E1.get())
                width = int(E2.get())
                rows = []
                for i in range(height):  # Rows
                    cols = []
                    for j in range(width):  # Columns
                        b = tk.Entry(root9, text="")
                        b.grid(row=i, column=j)
                        cols.append(b)
                    rows.append(cols)

                def Kmeans_seg3():
                    global Kernel
                    Kernel = []
                    for row in rows:
                        for col in row:
                            Kernel.append(float(col.get()))

                    Kernel = np.array(Kernel, np.uint8)
                    Kernel = np.reshape(Kernel, (height, width))
                    km = KMeans(n_clusters=3)
                    km.fit(vectorized)
                    img_seg=km.cluster_centers_
                    img_seg=img_seg[km.labels_]
                    img_seg=img_seg.reshape(img.shape)
                    # opening the image
                    opening = cv2.morphologyEx(img_seg, cv2.MORPH_OPEN,
                           Kernel, iterations=1)
                    dilatation = cv2.dilate(opening, Kernel,iterations = 1)
                    q = cv2.subtract(dilatation,opening) 
                    ax2.imshow(img_seg, cmap='gray')
                    ax2.set_title("Segmented Image")

                    fig.canvas.draw_idle()

                btn1 = tk.Button(root9, bg='#0e3a53', fg='#aaf0c1', text='   Set   ', padx=20, bd='5',
                                 command=Kmeans_seg3)
                btn1.grid(row=height + 1, column=0)
                root9.mainloop()

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=900, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            L1 = tk.Label(root8, text="Rows:", bg='#0e3a53', fg='#aaf0c1', bd=5)
            L1.place(x=400, y=650)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=440, y=650)

            L2 = tk.Label(root8, text="Column:", bg='#0e3a53', fg='#aaf0c1', bd=5)
            L2.place(x=570, y=650)
            E2 = tk.Entry(root8, bd=5)
            E2.place(x=630, y=650)

            btn2 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   Apply   ', padx=20, bd='1',
                             command=Kmeans_seg2)
            btn2.place(x=730, y=650)

            ax2.imshow(img, cmap='gray')
            ax2.set_title('Original Image')
            ax1.set_title('Original Image')

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("channel ", x1 + 1))

    else:
        Dimension_Number = [("channel", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a channel:", font=('Franklin Gothic Demi Cond', 11)).place(x=0,y=0)
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.place(x=150,y=0)
        numberChosen1.current(0)

        btn25 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   One channel   ', padx=40, bd='10',
                        command=Kmeans_seg1)
        btn25.place(x=320,y=0)

        
        btn26 = tk.Button(root8, bg='#0e3a53', fg='#aaf0c1', text='   Grayscale   ', padx=40, bd='10',
                        command=Kmeans_seg1)
        btn26.place(x=520,y=0)

    def Quit():
        root8.quit()
        root8.destroy()

    button3 = tk.Button(master=root8, bg='#0e3a53', fg='#aaf0c1', text='       Quit        ', padx=40,
                       bd='10', command=Quit)
    button3.place(x=720,y=0)

    root8.mainloop()

    
############################# Unet #####################################
    
def meanshift():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("Traitement des imageries médicales")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
   

    def meanshif():
        meanshif=3
        if len(Original_image_Size) > 2:
           
            img = Original_Image[:, :, meanshif - 1]
            img = np.array(img)
            #model 
    return 0
        
            

############################# Sup'Com logo #############################

   
image1 = Image.open('Title.png')
copy_of_image1 = image1.copy()
photo1 = ImageTk.PhotoImage(image1)
label1 = ttk.Label(window, image = photo1)
label1.place(x=0, y=0)


############################# Work prepared by  ###############################
label3=tk.Label(master=window, text = "Aymen Bejaoui", bg="red", fg="white",
                     font=("times new roman", 20, "bold"))
label3.place(x=470, y=0)
    
window.title("Traitement des imageries médicales")
############################### Menu #####################################
menubar1 = tk.Menu(window)

filemenu = tk.Menu(menubar1, tearoff=0,activeborderwidth=4,font=('Franklin Gothic Demi Cond', 11))
filemenu.add_command(label="New", command=OPEN)
filemenu.add_command(label="Open", command=OPEN)
filemenu.add_command(label="Save", command=OPEN)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=window.quit)


Histogrammenu = tk.Menu(menubar1, tearoff=0,activeborderwidth=4,font=('Franklin Gothic Demi Cond', 11))

Histogrammenu.add_command(label="Show Histogram", command=Show_Histogram1)

menubar1.add_cascade(label="Histogram", menu=Histogrammenu)


Filteringmenu = tk.Menu(menubar1, tearoff=0,activeborderwidth=4,font=('Franklin Gothic Demi Cond', 11))

Filteringmenu.add_command(label="Averaging Filter", command=AverageFilter)
Filteringmenu.add_command(label="Median Filtering", command=MedianFilter)




menubar1.add_cascade(label="Filtering", menu=Filteringmenu)


segmenu = tk.Menu(menubar1,tearoff=0, activeborderwidth=4,  font=('Franklin Gothic Demi Cond', 11))

trmenu = tk.Menu(menubar1,tearoff=0, activeborderwidth=4, font=('Franklin Gothic Demi Cond', 11))
segmenu.add_cascade(label="THresholding", menu=trmenu)
trmenu.add_command(label="Simple thresholding", command=thresholding)

regionmenu = tk.Menu(menubar1,tearoff=0, activeborderwidth=4, font=('Franklin Gothic Demi Cond', 11))
segmenu.add_cascade(label="Segmentation based Region", menu=regionmenu)
regionmenu.add_command(label="Kmeans", command=Kmeans_seg)

segmenu.add_command(label="Meanshift", command=meanshift )


menubar1.add_cascade(label="Segmentation", menu=segmenu)

editmenu = tk.Menu(menubar1,tearoff=0, activeborderwidth=4, font=('Franklin Gothic Demi Cond', 11))
editmenu.add_command(label="Help", command=None)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=None)
editmenu.add_command(label="Delete", command=None)
editmenu.add_command(label="Select All", command=None)

menubar1.add_cascade(label="Edit", menu=editmenu)


window.config(menu=menubar1)
window.mainloop()
