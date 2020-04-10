import math
import os
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as mb
from PIL import Image, ImageFilter
import cv2
import numpy as nm
from skimage.util import random_noise


# For creating applet - GUI
window = tkinter.Tk()
window.title("CSC8208- Processing")
window.geometry("300x360+0+0")
window.resizable(0, 0)
window.eval('tk::PlaceWindow . center')
# ---- End Window----
# First layout frame --------


# Heading label and other select file buttons and location label
Label1 = Label(window, text="Welcome to Image Perturbation ", pady=20, justify=LEFT)
Label1.config(font=("Helvetica", 13))
Label1.place(x=30, y=10)
LctnLbl = Label(window, wraplength=300, fg="red")

label2 = Label(window, text="Select Operation")
label2.configure(font="Arial 10 underline")
label2.place(x=10, y=80)
Gschkvar = IntVar()
Rtchkvar = IntVar()
Blrchkvar = IntVar()
Dschkvar = IntVar()
Rplchkvar = IntVar()
Gauchkvar = IntVar()
Opxchkvar = IntVar()
gsinputStr = tkinter.StringVar()
RtinputStr = tkinter.StringVar()
BlrinputStr = tkinter.StringVar()
CrpinputStr = tkinter.StringVar()
RplinputStr = tkinter.StringVar()
gausinputStr = tkinter.StringVar()
OpxlinputStr = tkinter.StringVar()
GsChkbk = Checkbutton(window, text="Grayscale", variable=Gschkvar, onvalue=1).place(x=20, y=120)
GsInput = Entry(window, width=7, textvariable=gsinputStr).place(x=20, y=150)
gsinputStr.set("L")
RtChkbk = Checkbutton(window, text="Rotate", variable=Rtchkvar, onvalue=1).place(x=100, y=120)
RtnInput = Entry(window, width=7, textvariable=RtinputStr).place(x=100, y=150)
RtinputStr.set("45")
BlrChkbk = Checkbutton(window, text="Blur", variable=Blrchkvar, onvalue=1).place(x=160, y=120)
BlrInput = Entry(window, width=7, textvariable=BlrinputStr).place(x=160, y=150)
BlrinputStr.set("2")
DsChkbk = Checkbutton(window, text="Distort", variable=Dschkvar, onvalue=1).place(x=220, y=120)  # crop and blur
CrpInput = Entry(window, width=12, textvariable=CrpinputStr).place(x=220, y=150)
CrpinputStr.set("13, 17, 26, 21")
RplChkbk = Checkbutton(window, text="Ripple", variable=Rplchkvar, onvalue=1, fg="blue").place(x=20, y=180)
RplInput = Entry(window, width=7, textvariable=RplinputStr).place(x=20, y=205)
RplinputStr.set("270")
GauChkbk = Checkbutton(window, text="S & P", variable=Gauchkvar, onvalue=1, fg="blue").place(x=100, y=180)
GauInput = Entry(window, width=7, textvariable=gausinputStr).place(x=100, y=205)
gausinputStr.set("0.5")
OpxChkbk = Checkbutton(window, text="One Pixel", variable=Opxchkvar, onvalue=1, fg="blue").place(x=160, y=180)
OpxlInput = Entry(window, width=12, textvariable=OpxlinputStr).place(x=160, y=205)
OpxlinputStr.set("20, 20, 0, 0, 0")


# Get the file dialog window and obtains the folder contains the input image
def browse():
    clear(LctnLbl)
    browseLctn = filedialog.askdirectory(title="Choose Input Folder")
    LctnLbl.configure(text="Source is : " + browseLctn, justify=LEFT)
    LctnLbl.place(x=5, y=260)
    return browseLctn


# To clear the "Source" label for initiating the correct location
def clear(type):
    type.configure(text="")


# Function to change the image into grayscale with the help of PIL package
def grscl(img, input):
    grSclimg = img.convert(input)
    return grSclimg


# Function to rotate the image with respect to certain degrees with the help of PIL package
def rotn(img, input):
    input = int(input)
    rotated = img.rotate(input)
    return rotated


# Function to blur the image with respect to certain radius amount with the help of PIL package
def blurImg(img, input):
    input = int(input)
    blurImage = img.filter(ImageFilter.GaussianBlur(radius=input))
    return blurImage


# Function to crop the image for a area and apply blur and then paste
# it in the same location with the help of PIL package
def CropNblur(img, List):
    cropImage = img.crop(List)
    cropImage2 = img.crop((31, 1, 35, 15))
    cropNdBlur = cropImage.filter(ImageFilter.GaussianBlur(radius=10))
    cropNdBlur2 = cropImage2.filter(ImageFilter.GaussianBlur(radius=5))
    img.paste(cropNdBlur, List)
    img.paste(cropNdBlur2, (31, 1, 35, 15))
    return img


# Function to apply ripple effect on both horizontal and
# vertical axis of an image with the help of openCV package
def wave(img, imgNm, input):
    input = int(input)
    img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    rows, cols = img.shape
    WavImg = nm.zeros(img.shape, dtype=img.dtype)

    for i in range(rows):
        for j in range(cols):
            offset_x = int(15.0 * math.sin(1 * 3.14 * i / input))
            offset_y = int(15.0 * math.cos(1 * 3.14 * j / 150))
            if i + offset_y < rows and j + offset_x < cols:
                WavImg[i, j] = img[(i + offset_y) % rows, (j + offset_x) % cols]
            else:
                WavImg[i, j] = 0
    changedImg = Image.fromarray(nm.uint8(WavImg))
    changedImg.save("Transformed/Ripple/" + imgNm)


# Function to add Salt and Pepper in the image. It is a kind of distorting the
# image to some amount with the help of OpenCV package
def saltNpepper(img, imgNm, input):
    input = float(input)
    noisyImgInpt = cv2.imread(img)
    noisyImg = random_noise(noisyImgInpt, mode='s&p', amount=input)
    noisyImg = nm.array(255 * noisyImg, dtype='uint8')
    cv2.imwrite("Transformed/saltNppr/" + imgNm, noisyImg)
    cv2.waitKey(0)


# Function to change a particular pixel of an image
# and save it in the directory with the help of openCV package
def OpxlAtk(pxlValue, img, name):
    img = cv2.imread(img)
    x, y, *rgb = pxlValue
    img[x, y] = rgb
    cv2.imwrite("Transformed/OnePixel/" + name, img)
    cv2.waitKey(0)


# Function to execute the corresponding perturbation type methods
# based on the checkbox values that user has selected in the GUI
def process():
    try:
        BrwsLctn = browse()
        arr = os.listdir(BrwsLctn)
        OpxChng = OpxlinputStr.get()
        DstrtChng = CrpinputStr.get()

        OpxChList = OpxChng.split(",")
        Opxllist = []
        for i in OpxChList:
            Opxllist.append(int(i))

        DstChList = DstrtChng.split(",")
        Dstllist = []
        for i in DstChList:
            Dstllist.append(int(i))
        for i in arr:
            EchImgLctn = BrwsLctn + "/" + i
            img = Image.open(EchImgLctn)
            if Gschkvar.get() == 1:
                img = grscl(img, gsinputStr.get())
            if Rtchkvar.get() == 1:
                img = rotn(img, RtinputStr.get())
            if Blrchkvar.get() == 1:
                img = blurImg(img, BlrinputStr.get())
            if Dschkvar.get() == 1:
                img = CropNblur(img, Dstllist)
            if Gauchkvar.get() == 1:
                saltNpepper(EchImgLctn, i, gausinputStr.get())
            if Rplchkvar.get() == 1:
                wave(EchImgLctn, i, RplinputStr.get())
            if Opxchkvar.get() == 1:
                OpxlAtk(Opxllist, EchImgLctn, i)

            img.save("Transformed/Output/" + i)

        # Option selected other than blue checkboxes in the GUI are stored in the standard folder "output".
        if Gschkvar.get() == 1 or Rtchkvar.get() == 1 or Blrchkvar.get() == 1 or Dschkvar.get() == 1:
            mb.showinfo(title="Info", message="Image(s) are stored in the Output folder of Transformed directory")
        # Options  selected in blue are stored in separate folder.Where these indicates that images can
        # processed only one at a time.
        if Rplchkvar.get() == 1 or Gauchkvar.get() == 1 or Opxchkvar.get() == 1:
            mb.showinfo(title="Info", message="Image(s) are stored in the appropriate folders of Transformed directory")
        DstLbl = Label(window, text="Destination is : Transformed/..", fg="green").place(x=5, y=310)

    except:
        mb.showwarning("Warning", "Please select input folder!!! Try again")


executeBtn = Button(window, text="Process", bg="red", command=process).place(x=200, y=230)

window.mainloop()
