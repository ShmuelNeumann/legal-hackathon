import tkinter as tk
from tkinter.filedialog import askopenfile
import cv2
from PIL import ImageTk,Image


class Data:
    """
    Class to represent the form data for all the screens in the application.
    """

    def __init__(self):
        self.image_and_text_outputs = [None, None, None]
        self.image_file_path = ""
        self.image_text = ""

    def get_image_and_text_outputs(self):
        """
        Desc:
            getter method for the main list output for this class [isImage: bool, file_path:str,image_text: str]
        Inputs: N/A
        Return: N/A
        """
        return self.image_and_text_outputs

    def get_image_file_path(self):
        """
        Desc:
            getter method for images file path
        Inputs: N/A
        Return: N/A
        """

        return self.image_file_path

    def get_image_text(self):
        """
        Desc:
            getter method for images associated text
        Inputs: N/A
        Return:
            image_text: string value representing the text contained on an image.
        """
        return self.image_text

    def set_image_and_text_outputs(self,p1,p2,p3):
        """
        Desc:
            Method to set the list values in the form of [isImage: bool, file_path:str,image_text: str]
        Inputs:
            p1: bool value for whether we are comparing an image or just text
            p2: False for just text  or image path if comparing image
            p3: text either for the image or just the text.
        Return: N/A
        """
        self.image_and_text_outputs[0] = p1
        self.image_and_text_outputs[1] = p2
        self.image_and_text_outputs[2] = p3

    def set_image_file_path(self,file_path):
        """
        Desc:
            setter method to set the file_path for the image
        Inputs: N/A
        Return: N/A
        """
        self.image_file_path = file_path

    def set_image_text(self,image_text):
        """
        Desc:
            setter method to set the images printed text
        Inputs: N/A
        Return: N/A
        """
        self.image_text = image_text



# create an instance of formData class
formData = Data()
scaled_image_size = []


root = tk.Tk()
root.title("Trademark Checking Tool")
root.geometry("500x500")


# FUNCTIONS TO CALL TO TRANSITION BETWEEN PAGES
def home_to_image_and_text():
    """
    Desc:
        Function to transition the frame of the interface from the home frame, to the image_and_text frame
    Inputs: N/A
    Returns: N/A
    """
    home_page.pack_forget()
    image_and_image_text.pack(side= tk.TOP, anchor="w")
    pass

def home_to_text():
    """
    Desc:
        Function to transition the frame of the interface from the home frame, to the just_text frame
    Inputs: N/A
    Returns: N/A
    """
    home_page.pack_forget()
    just_text.pack(side= tk.TOP, anchor="w")

def image_and_text_to_home():
    """
    Desc:
        Function to transition the frame of the interface from the image_and_text frame, to the home frame
    Inputs: N/A
    Returns: N/A
    """
    # remove the image from the canvas
    canvas.delete("all")
    # delete the string in the image text
    text_label.config(text="")
    image_and_image_text.pack_forget()
    home_page.pack(side= tk.TOP, anchor="w")

def text_to_home():
    """
    Desc:
        Function to transition the frame of the interface from the just_text frame, to the home frame
    Inputs: N/A
    Returns: N/A
    """
    pass

# END OF TRANSITION FUNCTIONS



# SETTING UP THE DIFFERENT SCREENS IN THE APPLICATION
home_page = tk.Frame(root,width=500,height=500)
image_and_image_text = tk.Frame(root)
just_text = tk.Frame(root)

home_page.pack(side= tk.TOP, anchor="w")

# create the home_page of the application

# HOME PAGE HEADING
home_page_heading = tk.Label(home_page,text="Home Page of Trademark Application",font=('Helvatical bold',16))
home_page_heading.pack(side= tk.TOP, anchor="c", pady=(0,5))

# BUTTON TO TRANSITION TO THE IMAGE AND TEXT PAGE
transition_to_image_and_text = tk.Button(home_page,text="Compare Image", command=home_to_image_and_text)
transition_to_image_and_text.pack(side= tk.TOP, anchor="c", pady=(0,5),padx=5,fill="x")

# BUTTON TO TRANSITION TO THE TEXT ONLY PAGE
transition_to_text = tk.Button(home_page,text="Compare Text", command=home_to_text)
transition_to_text.pack(side= tk.TOP, anchor="c", pady=(0,5),padx=5,fill="x")





# IMAGE AND IMAGE TEXT INTERFACE ITEMS AND FUNCTIONS
def resize_image(path,sf):
    """
    Desc:
        This function rescales the image according to the scaling factor
    Inputs:
        path: string path to the original image to be resized
        sf: integer value between 1-100, will determine what size you want the image to be scaled to
    Returns:
        returns a numpy Array of the resized image.
    """
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
    """
    Desc:
        This function is responsible for opening an image file either jpg, or png.
    Inputs: N/A
    Returns: N/A
    """
    file_path = askopenfile(mode='r', filetypes=[('Image Files', 'jpg'),('Image Files', 'png')])
    if file_path is not None:
        formData.set_image_file_path(file_path.name)
        # resize the image to 10% of its original size
        resize_image(file_path.name,10)
        # display the resized image as the uploaded image.
        display_image_and_text(file_path.name)



# first part of the interface label for choose your image.
open_image_text_label = tk.Label(image_and_image_text, text="Choose your image",font=('Helvatical bold',16))
open_image_text_label.pack(side= tk.TOP, anchor="w", pady=(0,5))

# second part of interface tell the user the file format.

imageText = tk.Label(image_and_image_text,text='Upload image with extension png or jpg',font=('Helvatical bold',14))
imageText.pack(side= tk.TOP, anchor="w",padx=10, pady=(0,5))

# third part is a button to upload the image file opens the file explorer.

uploadButton = tk.Button(image_and_image_text,text='Upload File',command = open_file)
uploadButton.pack(side= tk.TOP, anchor="w",padx=10,pady=(0,5))


# create a label
# first part of the interface label for choose your image.
enter_image_text_label = tk.Label(image_and_image_text, text="Enter Image text",font=('Helvatical bold',16))
enter_image_text_label.pack(side= tk.TOP, anchor="w",pady=(0,5))
# create the text box for the user to enter the image text.
text_box = tk.Text(image_and_image_text,height=1,width=40)
text_box.pack(side= tk.TOP, anchor="w",padx=10,pady=(0,5))

def get_textbox_text():
    """
    Desc:
        this function is responsible for retrieving the text from the image, from the textbox.
        It also deletes the submitted text for a clean textbox for next time.
    Inputs: N/A
    Returns: N/A
    """

    image_text = text_box.get("1.0",tk.END)
    display_text(image_text)
    text_box.delete("1.0", tk.END)

# submit text button
get_text_button = tk.Button(image_and_image_text,text='Submit Image Text',command = get_textbox_text)
get_text_button.pack(side= tk.TOP, anchor="w",padx=10,pady=(0,5))



def getInput(button:tk.Button):
    """
    Desc:
        this function passes the input in the form of [True, file_path, image_text] if the data is coming from the image_and_image_text screen.
        and passes the input in the form of [False,False, text] if it coming just from the text screen of the application.
    Inputs:
        button: The button instance that is being clicked to submit the form data.
    Returns:
        the list in the form of [True, file_path, image_text] if its coming from the image_and_image_text frame or
        the list in the form of [False, False, text] if its coming from the just_text screen.
    """
    if button.master == image_and_image_text:
        formData.set_image_and_text_outputs(True,formData.get_image_file_path(),formData.get_image_text())
    elif button.master == just_text:
        formData.set_image_and_text_outputs(False, False, formData.get_image_text())

    print(formData.get_image_and_text_outputs())
    return formData.get_image_and_text_outputs()




# submit both image and text for processing
send_image_and_text_for_processing_btn = tk.Button(image_and_image_text,text="Send Image and Text for Processing")
send_image_and_text_for_processing_btn.config(command=lambda: getInput(send_image_and_text_for_processing_btn))
send_image_and_text_for_processing_btn.pack(side=tk.TOP, anchor="w",padx=5,pady=(0,5))

# heading for displaying the chosen image
uploaded_image_label = tk.Label(image_and_image_text, text="Current Uploaded image", font=('Helvatical bold', 16))
uploaded_image_label.pack(side=tk.TOP, anchor="w",pady=(0,5))

# create the canvas for our image that has been uploaded.
canvas = tk.Canvas(image_and_image_text, width=100, height=100)
canvas.pack(side=tk.TOP, anchor="w", padx=10,pady=(0,5))

uploaded_image_text_label = tk.Label(image_and_image_text, text="Current uploaded image text", font=('Helvatical bold', 16))
uploaded_image_text_label.pack(side=tk.TOP, anchor="w",pady=(0,5))

text_label = tk.Label(image_and_image_text, text="", font=('Helvatical bold', 14))
text_label.pack(side=tk.TOP, anchor="w", padx=10,pady=(0,5))




def display_text(image_text):
    """
    Desc:
        this function displays the text to the screen showing the user the image text that they entered
    Inputs:
        image_text: a string representing the images text.
    Returns: N/A
    """
    # current uploaded image text
    text_label.config(text=image_text)
    formData.set_image_text(image_text.strip("\n"))


def display_image_and_text(file_path):
    """
    Desc:
        this function updates the canvas with a preview of the newly uploaded image.
    Inputs:
        file_path: a string representing the path to the image file.
    Returns: N/A
    """
    # create the image size dynamically based on what the image scaling resizes the image to
    canvas.config(width=scaled_image_size[0],height=scaled_image_size[1])
    # get the numpy array of the resized image
    resized_image = Image.fromarray(resize_image(file_path, 10))

    ph = ImageTk.PhotoImage(resized_image)

    canvas.image = ph  # to prevent the image garbage collected.
    canvas.create_image((0, 0), image=ph, anchor='nw')



btn_image_and_text_to_home = tk.Button(image_and_image_text,text="Back to home page",command=image_and_text_to_home)
btn_image_and_text_to_home.pack(side=tk.TOP, anchor="w", padx=10,pady=(0,5))




# JUST TEXT COMPARISON

just_text_page_heading = tk.Label(just_text,text="Enter text to be tested", font=('Helvatical bold', 16))
just_text_page_heading.pack(side=tk.TOP, anchor="w",pady=(0,5))


# run the interface.
root.mainloop()





