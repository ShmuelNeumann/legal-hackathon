import cv2 as cv
from PIL import Image, ImageTk
import tkinter
from tkinter.filedialog import askopenfile

root = tkinter.Tk()
imageText = tkinter.Label(root,text='Upload logo with extension .jpg')
imageText.grid(row=0, column=0, padx=10)

uploadImagebtn = tkinter.Button(root,text ='Choose File',command = lambda:open_file())
uploadImagebtn.grid(row=0, column=1)

def open_file():
    file_path = askopenfile(mode='r', filetypes=[('Image Files', 'jpg')])
    if file_path is not None:
        img = cv.imread(file_path.name)

        b, g, r = cv.split(img)
        img = cv.merge((r, g, b))

        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)

        # Put it in the display window
        tkinter.Label(root, image=imgtk).grid(row=1, column=2)
        # show image
        cv.imshow('Image', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

root.mainloop()















