from tkinter import *
from tkinter import filedialog
import cv2

def loadImage():
    Tk().withdraw()  #Cierro la ventana que me crea tkinter y solo molesta
    filepath = filedialog.askopenfilename(filetypes=[("Image files","*.png"), ("Image files","*.jpg")]) #Pido imagen
    return cv2.imread(filepath, cv2.IMREAD_GRAYSCALE) #Cargo con el filepath la imagen y la devuelvo

def saveImage(img):
    Tk().withdraw()  # Cierro la ventana que me crea tkinter y solo molesta
    filepath = filedialog.asksaveasfilename(filetypes=[("Image files","*.png")])
    cv2.imwrite(filepath + '.png', img) #Guardo imagen como nombre_gray