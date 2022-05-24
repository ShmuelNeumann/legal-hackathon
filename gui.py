from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import time
root = Tk()

def open_file():
    file_path = askopenfile(mode='r', filetypes=[('Image Files', 'jpg')])
    if file_path is not None:
        pass


imageText = Label(
    root,
    text='Upload logo with extension .jpg'
    )
imageText.grid(row=0, column=0, padx=10)

uploadImagebtn = Button(
    root,
    text ='Choose File',
    command = lambda:open_file()
    )
uploadImagebtn.grid(row=0, column=1)


uploadButton = Button(
    root,
    text='Upload Files',
    command = lambda:uploadFiles()
    )
uploadButton.grid(row=3, columnspan=3, pady=10)

def uploadFiles():
    pb1 = Progressbar(
        root,
        orient=HORIZONTAL,
        length=300,
        mode='determinate'
        )
    pb1.grid(row=4, columnspan=3, pady=20)
    for i in range(5):
        root.update_idletasks()
        pb1['value'] += 20
        time.sleep(1)
    pb1.destroy()
    Label(root, text='File Uploaded Successfully!', foreground='green').grid(row=4, columnspan=3, pady=10)

root.mainloop()





