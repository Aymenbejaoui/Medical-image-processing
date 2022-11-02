# Medical-image-processing
Interactive dashboard for medical image analysis with filtering and segmentation techniques to detect the region of interest in a human vocal cord image.


main Libraries : 
Tkinter : Create and manipulate a Graphical User Interface widgets.
Matplotlib: Displays graphs and histograms of selected images at different scales.
PyLab : Use Matplotlib Module and Numpy as an object-oriented plotting library of Python.
Skimage : An open source Python package designed for image preprocessing.Equivalent to Scikit Learn library for machine learning algorithms.
Sklearn.cluster : For unsupervised image segmentation techniques.


Setup 1 : Choose an image file (png,jpeg,jpg,tif...) 

Open function : Use the path image to open a tkinter window after that that you can observ your image with simple click.

Setup 2 : Visualize image's Histogram : 
          Histogramms helps parsing the distribution of pixels for a given image on a gray scale or with multiple channels(Supported within this app).
          This is an important measure because it can help detect the intermediate region of an object and often contributes to the improvement of the image by 
          equalizing probability distribution.
          
Setup 3: Choose a filtering method :

Median_filter and mean_filer: After uploading the necessary image the menu upfront will help you choosing between median or averaging filter to avoid the noise (high 
                               frequency pixels).
                              !! :An average filter reduce the noise by summing to its (nearly) zero average value or neighbors. On the other hand, 
                              a median filter eliminates noise by ignoring it.
                              
Setup 4 :Segmentation :

Canny : Filter for edge detection.

Thresholding : or simply image Binarization :replacing the gray levels of an image by a set of pixels taking the value 255 or 0 depending on whether its initial value is 
               lower or higher than a value defined as a threshold. 
               
Kmeans : Unsupervised machine learning technics that consists on finding patterns into data without any given labels.excepts data in our case are pixels
            and their neighbors.   
            
            
If you want to run this app you just have to set the path of images and set a python working environement with the necessary librairies.
            
