from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import cv2
from PIL import ImageTk,Image

root = Tk()
root.title("Trademark Checking Tool")
root.geometry("500x500")

image_file_path = ""
image_text = ""
scaled_image_size = []



def resize_image(path,sf):
    src = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

    # percent by which the image is resized
    scale_percent = sf

    # calculate the scaled percent percent of original dimensions
    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)

    for width_height in list(dsize):
        scaled_image_size.append(width_height)

    # resize image
    output = cv2.resize(src, dsize)
    return output


def open_file():
    file_path = askopenfile(mode='r', filetypes=[('Image Files', 'jpg'),('Image Files', 'png')])
    if file_path is not None:
        resize_image(file_path.name,10)
        display_image(file_path.name)




# first part of the interface label for choose your image.
open_image_text_label = Label(root, text="Choose your image",font=('Helvatical bold',16))
open_image_text_label.pack(side= TOP, anchor="w", pady=(0,5))

# second part of interface tell the user the file format.

imageText = Label(root,text='Upload image with extension png or jpg',font=('Helvatical bold',14))
imageText.pack(side= TOP, anchor="w",padx=10, pady=(0,5))

# third part is a button to upload the image file opens the file explorer.

uploadButton = Button(root,text='Upload File',command = open_file)
uploadButton.pack(side= TOP, anchor="w",padx=10,pady=(0,5))


# create a label
# first part of the interface label for choose your image.
enter_image_text_label = Label(root, text="Enter Image text",font=('Helvatical bold',16))
enter_image_text_label.pack(side= TOP, anchor="w",pady=(0,5))
# create the text box for the user to enter the image text.
text_box = Text(root,height=1,width=40)
text_box.pack(side= TOP, anchor="w",padx=10,pady=(0,5))

def get_textbox_text():
    image_text = text_box.get("1.0",END)
    display_text(image_text)
    text_box.delete("1.0", END)

# submit text button
get_text_button = Button(root,text='Submit Image Text',command = get_textbox_text)
get_text_button.pack(side= TOP, anchor="w",padx=10,pady=(0,5))

# heading for displaying the chosen image
uploaded_image_label = Label(root, text="Current Uploaded image", font=('Helvatical bold', 16))
uploaded_image_label.pack(side=TOP, anchor="w",pady=(0,5))

# create the canvas for our image that has been uploaded.
canvas = Canvas(root, width=100, height=100)
canvas.pack(side=TOP, anchor="w", padx=10,pady=(0,5))

uploaded_image_text_label = Label(root, text="Current uploaded image text", font=('Helvatical bold', 16))
uploaded_image_text_label.pack(side=TOP, anchor="w",pady=(0,5))

text_label = Label(root, text="", font=('Helvatical bold', 14))
text_label.pack(side=TOP, anchor="w", padx=10,pady=(0,5))




def display_text(image_text):
    # current uploaded image text
    text_label.config(text=image_text)


def display_image(file_path):
    # create the image size dynamically based on what the image scaling resizes the image to
    canvas.config(width=scaled_image_size[0],height=scaled_image_size[1])
    # get the numpy array of the resized image
    resized_image = Image.fromarray(resize_image(file_path, 10))

    ph = ImageTk.PhotoImage(resized_image)

    canvas.image = ph  # to prevent the image garbage collected.
    canvas.create_image((0, 0), image=ph, anchor='nw')

# run the interface.
root.mainloop()





