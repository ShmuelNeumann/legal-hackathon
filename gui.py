import tkinter as tk
from tkinter.filedialog import askopenfile
import cv2
from PIL import ImageTk,Image
import matplotlib.pyplot as plt
from main_flow import get_image

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

def initialise_tkinter():
    return_dictionary = {}
    # create an instance of formData class
    formData = Data()
    return_dictionary['form_data'] = formData
    scaled_image_size = []
    return_dictionary['scaled_image_size'] = scaled_image_size

    root = tk.Tk()
    return_dictionary['root_window'] = root
    root.title("Trademark Checking Tool")
    root.geometry("800x800")

    # SETTING UP THE DIFFERENT SCREENS IN THE APPLICATION

    home_page = tk.Frame(root, width=500, height=500)
    return_dictionary['home_page_frame'] = home_page
    image_and_image_text = tk.Frame(root, width=800, height=500)
    return_dictionary['image_and_image_text_frame'] = image_and_image_text
    just_text = tk.Frame(root, width=500, height=500)
    return_dictionary['just_text_frame'] = just_text

    # set the initial frame of the application.
    # HOME PAGE HEADING
    home_page_heading = tk.Label(home_page, text="Home Page of Trademark Application", font=('Helvatical bold', 16))
    home_page_heading.pack(side=tk.TOP, anchor="c", pady=(0, 5))
    return_dictionary['home_page_heading_label'] = home_page_heading

    # BUTTON TO TRANSITION TO THE IMAGE AND TEXT PAGE
    transition_to_image_and_text = tk.Button(home_page, text="Compare Image")
    transition_to_image_and_text.config(
        command=lambda: transition_between_frames(return_dictionary, home_page, image_and_image_text))
    transition_to_image_and_text.pack(side=tk.TOP, anchor="c", pady=(0, 5), padx=5, fill="x")
    return_dictionary['transition_btn_home_to_image_and_text'] = transition_to_image_and_text

    # BUTTON TO TRANSITION TO THE TEXT ONLY PAGE
    transition_to_text = tk.Button(home_page, text="Compare Text")
    transition_to_text.config(command=lambda: transition_between_frames(return_dictionary, home_page, just_text))
    transition_to_text.pack(side=tk.TOP, anchor="c", pady=(0, 5), padx=5, fill="x")
    return_dictionary['transition_btn_home_to_text'] = transition_to_text

    home_page.pack(side=tk.TOP, anchor="w")
    return_dictionary['active_frame'] = home_page

    # create the home_page of the application

    root.mainloop()
    return return_dictionary

def initialise_image_and_text(dictionary):
    image_and_image_text = dictionary.get('image_and_image_text_frame')
    dictionary['active_frame'] = image_and_image_text
    formData = dictionary.get('form_data')
    home_page = dictionary.get('home_page_frame')
    scaled_image_size = dictionary.get('scaled_image_size')

    # first part of the interface label for choose your image.
    open_image_text_label = tk.Label(image_and_image_text, text="Choose your image", font=('Helvatical bold', 16))
    open_image_text_label.grid(row=0,column=0)
    dictionary['choose_image_text_label'] = open_image_text_label

    # second part of interface tell the user the file format.


    # third part is a button to upload the image file opens the file explorer.

    uploadButton = tk.Button(image_and_image_text, text='Upload File',
                             command=lambda: open_file(formData, canvas, scaled_image_size))
    uploadButton.grid(row=1,column=0)
    dictionary['upload_image_btn'] = uploadButton

    # vertical formatting space
    vertical_space_1 = tk.Label(image_and_image_text,text="")
    vertical_space_1.grid(row=2,column=0)

    # create a label
    # first part of the interface label for choose your image.
    enter_image_text_label = tk.Label(image_and_image_text, text="Enter Image text", font=('Helvatical bold', 16))
    enter_image_text_label.grid(row=3,column=0)
    dictionary['enter_image_text_label'] = enter_image_text_label

    # create the text box for the user to enter the image text.
    text_box = tk.Text(image_and_image_text, height=1, width=40)
    text_box.grid(row=4,column=0)
    dictionary['enter_image_textbox'] = text_box

    # submit text button
    get_text_button = tk.Button(image_and_image_text, text='Submit Image Text',
                                command=lambda: get_textbox_text(text_box, formData, text_label))
    get_text_button.grid(row=5,column=0)
    dictionary['submit_text_btn'] = get_text_button



    # heading for displaying the chosen image
    uploaded_image_label = tk.Label(image_and_image_text, text="Current Uploaded image", font=('Helvatical bold', 16))
    uploaded_image_label.grid(row=0,column=1)
    dictionary['heading_display_chosen_image_label'] = uploaded_image_label

    # create the canvas for our image that has been uploaded.
    canvas = tk.Canvas(image_and_image_text, width=100, height=100)
    canvas.grid(row=2,column=1)
    dictionary['preview_image_canvas'] = canvas

    vertical_space_2 = tk.Label(image_and_image_text,text="")
    vertical_space_2.grid(row=6,column=0)

    uploaded_image_text_label = tk.Label(image_and_image_text, text="Current uploaded image text",
                                         font=('Helvatical bold', 16))
    uploaded_image_text_label.grid(row=3,column=1)
    dictionary['upload_image_text_label'] = uploaded_image_text_label

    text_label = tk.Label(image_and_image_text, text="", font=('Helvatical bold', 14))
    text_label.grid(row=4,column=1)
    dictionary['preview_image_text_label'] = text_label

    # submit both image and text for processing
    send_image_and_text_for_processing_btn = tk.Button(image_and_image_text, text="Send Image and Text for Processing",
                                                       command=lambda: getInput(dictionary))
    send_image_and_text_for_processing_btn.grid(row=9,column=1)
    dictionary['btn_submit_text_and_image'] = send_image_and_text_for_processing_btn

    image_and_image_text.pack(side=tk.TOP, anchor="w")
    # JUST TEXT COMPARISON


# FUNCTIONS TO CALL TO TRANSITION BETWEEN PAGES
def transition_between_frames(dictionary,current_frame, destination_frame):
    """
    Desc:
        Function to transition the frame of the interface from the home frame, to the image_and_text frame
    Inputs: N/A
    Returns: N/A
    """
    current_frame.pack_forget()
    if destination_frame == dictionary.get('just_text_frame'):
        initialise_just_text(dictionary)
    if destination_frame == dictionary.get('image_and_image_text_frame'):
        initialise_image_and_text(dictionary)

# IMAGE AND IMAGE TEXT INTERFACE ITEMS AND FUNCTIONS
def resize_image(path,sf,scaled_image_size):
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

    current_width = src.shape[1]
    current_height = src.shape[0]

    scaling_fac_width = current_width/100
    scaling_fac_height = scaling_fac_width


    width = int(current_width/scaling_fac_width)
    height = int(current_height/scaling_fac_height)

    # dsize
    dsize = (width, height)

    for width_height in list(dsize):
        scaled_image_size.append(width_height)

    # resize image
    output = cv2.resize(src, dsize)
    return output


def open_file(formData,canvas,scaled_image_size):
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
        resize_image(file_path.name,10,scaled_image_size)
        # display the resized image as the uploaded image.
        display_image_and_text(file_path.name,canvas,scaled_image_size)

def get_textbox_text(text_box,formData,text_label):
    """
    Desc:
        this function is responsible for retrieving the text from the image, from the textbox.
        It also deletes the submitted text for a clean textbox for next time.
    Inputs: N/A
    Returns: N/A
    """

    image_text = text_box.get("1.0",tk.END)
    display_text(formData,image_text,text_label)
    text_box.delete("1.0", tk.END)

def getInput(dictionary):
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

    current_frame = dictionary.get('active_frame')
    form_data = dictionary.get('form_data')
    root_window = dictionary.get('root_window')

    if current_frame == dictionary.get('image_and_image_text_frame'):
        form_data.set_image_and_text_outputs(True, form_data.get_image_file_path(), form_data.get_image_text())
        try:
            stop_main_loop(root_window)
        except tk._tkinter.TclError:
            pass
    elif current_frame == dictionary.get('just_text_frame'):
        form_data.set_image_and_text_outputs(False, False, form_data.get_image_text())
        try:
            stop_main_loop(root_window)
        except tk._tkinter.TclError:
            pass

    return form_data.get_image_and_text_outputs()



def display_text(formData,image_text,text_label):
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


def display_image_and_text(file_path, canvas, scaled_image_size):
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
    resized_image = Image.fromarray(resize_image(file_path, 10,scaled_image_size))

    ph = ImageTk.PhotoImage(resized_image)

    canvas.image = ph  # to prevent the image garbage collected.
    canvas.create_image((0, 0), image=ph, anchor='nw')





def stop_main_loop(window):
    window.destroy()

def show_results(dictionary,isImage,values,database):
    if isImage:
        # create new window
        results_window_dict = {}
        results_window = tk.Tk()
        results_window.title("Results Window")
        results_window.geometry("700x700")

        results_frame = tk.Frame(results_window, width=700, height=700)
        results_frame.pack(side=tk.TOP, anchor="w")

        # CREATE THE CANVASES FOR THE IMAGES
        # FIRST IMAGE HERE
        first_space = tk.Label(results_frame, text="", font=('Helvatical bold', 12))
        first_space.grid(row=0, column=1)

        heading_shape_sim = tk.Label(results_frame, text="Shape Comparison Results", font=('Helvatical bold', 16))
        heading_shape_sim.grid(row=1,column=1)

        shape_sim_space = tk.Label(results_frame, text="", font=('Helvatical bold', 12))
        shape_sim_space.grid(row=2,column=1)

        highest_shape_sim_canvas = tk.Canvas(results_frame, width=100, height=100)
        highest_shape_sim_canvas.grid(row=3,column=0)
        results_window_dict['highest_shape_sim_canvas'] = highest_shape_sim_canvas

        second_highest_shape_sim_canvas = tk.Canvas(results_frame, width=100, height=100)
        second_highest_shape_sim_canvas.grid(row=3,column=1)
        results_window_dict['second_highest_shape_sim_canvas'] = second_highest_shape_sim_canvas

        third_highest_shape_sim_canvas = tk.Canvas(results_frame, width=100, height=100)
        third_highest_shape_sim_canvas.grid(row=3,column=2)
        results_window_dict['third_highest_shape_sim_canvas'] = third_highest_shape_sim_canvas

        shape_similarity_1 = tk.Label(results_frame, text="Shape similarity: 74.67%", font=('Helvatical bold', 10))
        shape_similarity_1.grid(row=4,column=0)
        results_window_dict['shape_similarity_1'] = shape_similarity_1

        shape_similarity_2 = tk.Label(results_frame, text="Shape similarity: 53.57%", font=('Helvatical bold', 10))
        shape_similarity_2.grid(row=4,column=1)
        results_window_dict['shape_similarity_2'] = shape_similarity_2

        shape_similarity_3 = tk.Label(results_frame, text="Shape similarity: 34.29%", font=('Helvatical bold', 10))
        shape_similarity_3.grid(row=4,column=2)
        results_window_dict['shape_similarity_3'] = shape_similarity_3

        # COLOUR SIMILARITY
        second_space = tk.Label(results_frame, text="", font=('Helvatical bold', 12))
        second_space.grid(row=5, column=1)

        heading_colour_sim = tk.Label(results_frame, text="Colour Comparison Results", font=('Helvatical bold', 16))
        heading_colour_sim.grid(row=6,column=1)

        colour_sim_space = tk.Label(results_frame, text="", font=('Helvatical bold', 12))
        colour_sim_space.grid(row=7, column=1)

        highest_colour_sim_canvas = tk.Canvas(results_frame, width=100, height=100)
        highest_colour_sim_canvas.grid(row=8, column=0)
        results_window_dict['highest_colour_sim_canvas'] = highest_colour_sim_canvas

        second_highest_colour_sim_canvas = tk.Canvas(results_frame, width=100, height=100)
        second_highest_colour_sim_canvas.grid(row=8, column=1)
        results_window_dict['second_highest_colour_sim_canvas'] = second_highest_colour_sim_canvas

        third_highest_colour_sim_canvas = tk.Canvas(results_frame, width=100, height=100)
        third_highest_colour_sim_canvas.grid(row=8, column=2)
        results_window_dict['third_highest_colour_sim_canvas'] = third_highest_colour_sim_canvas


        colour_similarity_1 = tk.Label(results_frame, text="Colour similarity: 74.67%", font=('Helvatical bold', 10),anchor='w')
        colour_similarity_1.grid(row=9,column=0)
        results_window_dict['colour_similarity_1'] = colour_similarity_1

        colour_similarity_2 = tk.Label(results_frame, text="Colour similarity: 53.57%", font=('Helvatical bold', 10),anchor='w')
        colour_similarity_2.grid(row=9,column=1)
        results_window_dict['colour_similarity_2'] = colour_similarity_2

        colour_similarity_3 = tk.Label(results_frame, text="Colour similarity: 34.29%", font=('Helvatical bold', 10),anchor='w')
        colour_similarity_3.grid(row=9,column=2)
        results_window_dict['colour_similarity_3'] = colour_similarity_3


        # TEXT SIMILARITY

        third_space = tk.Label(results_frame, text="", font=('Helvatical bold', 12))
        third_space.grid(row=10, column=1)


        heading_text_sim = tk.Label(results_frame, text="Text Comparison Results", font=('Helvatical bold', 16))
        heading_text_sim.grid(row=11, column=1)

        text_sim_space = tk.Label(results_frame, text="", font=('Helvatical bold', 12))
        text_sim_space.grid(row=12, column=1)

        highest_text_sim_canvas = tk.Canvas(results_frame, width=100, height=100)
        highest_text_sim_canvas.grid(row=13, column=0)
        results_window_dict['highest_text_sim_canvas'] = highest_text_sim_canvas

        second_highest_text_sim_canvas = tk.Canvas(results_frame, width=100, height=100)
        second_highest_text_sim_canvas.grid(row=13, column=1)
        results_window_dict['second_highest_text_sim_canvas'] = second_highest_text_sim_canvas

        third_highest_text_sim_canvas = tk.Canvas(results_frame, width=100, height=100)
        third_highest_text_sim_canvas.grid(row=13, column=2)
        results_window_dict['third_highest_text_sim_canvas'] = third_highest_text_sim_canvas

        text_similarity_1 = tk.Label(results_frame, text="Text similarity: 74.67%", font=('Helvatical bold', 10),
                                       anchor='w')
        text_similarity_1.grid(row=14, column=0)
        results_window_dict['text_similarity_1'] = text_similarity_1

        text_similarity_2 = tk.Label(results_frame, text="Text similarity: 53.57%", font=('Helvatical bold', 10),
                                       anchor='w')
        text_similarity_2.grid(row=14, column=1)
        results_window_dict['text_similarity_2'] = text_similarity_2

        text_similarity_3 = tk.Label(results_frame, text="Text similarity: 34.29%", font=('Helvatical bold', 10),
                                       anchor='w')
        text_similarity_3.grid(row=14, column=2)
        results_window_dict['text_similarity_3'] = text_similarity_3

        color_list = get_colour_results(values)
        use_color_list = []
        color = 'color'
        shape_list = get_shape_results(values)
        use_shape_list = []
        shape = 'shape'
        text_list = get_text_results(values)
        use_text_list = []
        text = 'text'

        for pair in color_list:
            # ID
            use_color_list.append(pair[0])
            # SCORE
            use_color_list.append(pair[1])

        for pair in shape_list:
            # ID
            use_shape_list.append(pair[0])
            # SCORE
            use_shape_list.append(pair[1])

        for pair in text_list:
            # ID
            use_text_list.append(pair[0])
            # SCORE
            use_text_list.append(pair[1])

        for index in range(0, len(use_color_list), 2):
            set_score_and_image(use_color_list[index], use_color_list[index + 1], index, color, database,
                                results_window_dict)
        for index in range(0, len(use_shape_list), 2):
            set_score_and_image(use_shape_list[index], use_shape_list[index + 1], index, shape, database,
                                results_window_dict)
        for index in range(0, len(use_text_list), 2):
            set_score_and_image(use_text_list[index], use_text_list[index + 1], index, text, database,
                                results_window_dict)



        for index in range(0, len(use_color_list), 2):
            set_score_and_image(use_color_list[index], use_color_list[index + 1], index, color, database,results_window_dict)
        for index in range(0, len(use_shape_list), 2):
            set_score_and_image(use_shape_list[index], use_shape_list[index + 1], index, shape, database,results_window_dict)
        for index in range(0, len(use_text_list), 2):
            set_score_and_image(use_text_list[index], use_text_list[index + 1], index, text, database,results_window_dict)


        results_frame.mainloop()
    else:
        pass


def initialise_just_text(dictionary):
    just_text_frame = dictionary.get('just_text_frame')
    dictionary['active_frame'] = just_text_frame
    form_data = dictionary.get('form_data')

    heading_label  = tk.Label(just_text_frame, text="Input the trademark Text you wish to check", font=('Helvatical bold', 16))
    heading_label.pack(side=tk.TOP, anchor="w")

    just_text_box = tk.Text(just_text_frame, height=1, width=40)
    just_text_box.pack(side=tk.TOP, anchor="w", padx=10, pady=(0, 5))

    submit_just_text_btn = tk.Button(just_text_frame, text='Submit Image Text', command=lambda:get_textbox_text(just_text_box,form_data,display_current_text))
    submit_just_text_btn.pack(side=tk.TOP, anchor="w", padx=10, pady=(0, 5))

    current_text_label = tk.Label(just_text_frame, text="Current Text input", font=('Helvatical bold', 16))
    current_text_label.pack(side=tk.TOP, anchor="w")

    display_current_text = tk.Label(just_text_frame, text="", font=('Helvatical bold', 14))
    display_current_text.pack(side=tk.TOP, anchor="w", padx=10, pady=(0, 5))

    submit_just_text_for_processing = tk.Button(just_text_frame, text='Submit text for processing', command=lambda:getInput(dictionary))
    submit_just_text_for_processing.pack(side=tk.TOP, anchor="w", padx=10, pady=(0, 5))

    dictionary['submit_just_text_btn'] = submit_just_text_for_processing





    just_text_frame.pack(side=tk.TOP, anchor="w")

def get_colour_results(values):
    return values[1]

def get_shape_results(values):
    return values[0]

def get_text_results(values):
    return values[2]

def set_score_and_image(id,score,index,classification,database,interface_items):
    if classification == 'shape':
        if index == 0:
            path = get_image(str(id),database)
            resized_image = Image.fromarray(resize_image(path, 10, []))
            ph = ImageTk.PhotoImage(resized_image)
            canvas = interface_items.get('highest_shape_sim_canvas')
            canvas.image = ph  # to prevent the image garbage collected.
            canvas.create_image((0, 0), image=ph, anchor='nw')

            text_label = interface_items.get('shape_similarity_1')
            text_label.config(text=f"Shape similarity: {round(score*100,2)}%")

        elif index == 2:
            path = get_image(str(id), database)
            resized_image = Image.fromarray(resize_image(path, 10, []))
            ph = ImageTk.PhotoImage(resized_image)
            canvas = interface_items.get('second_highest_shape_sim_canvas')
            canvas.image = ph  # to prevent the image garbage collected.
            canvas.create_image((0, 0), image=ph, anchor='nw')

            text_label = interface_items.get('shape_similarity_2')
            text_label.config(text=f"Shape similarity: {round(score * 100, 2)}%")

        elif index == 4:
            path = get_image(str(id), database)
            resized_image = Image.fromarray(resize_image(path, 10, []))
            ph = ImageTk.PhotoImage(resized_image)
            canvas = interface_items.get('third_highest_shape_sim_canvas')
            canvas.image = ph  # to prevent the image garbage collected.
            canvas.create_image((0, 0), image=ph, anchor='nw')

            text_label = interface_items.get('shape_similarity_3')
            text_label.config(text=f"Shape similarity: {round(score * 100, 2)}%")

    elif classification == 'text':
        if index == 0:
            path = get_image(str(id), database)
            resized_image = Image.fromarray(resize_image(path, 10, []))
            ph = ImageTk.PhotoImage(resized_image)
            canvas = interface_items.get('highest_text_sim_canvas')
            canvas.image = ph  # to prevent the image garbage collected.
            canvas.create_image((0, 0), image=ph, anchor='nw')

            text_label = interface_items.get('text_similarity_1')
            text_label.config(text=f"Text similarity: {round(score * 100, 2)}%")

        elif index == 2:
            path = get_image(str(id), database)
            resized_image = Image.fromarray(resize_image(path, 10, []))
            ph = ImageTk.PhotoImage(resized_image)
            canvas = interface_items.get('second_highest_text_sim_canvas')
            canvas.image = ph  # to prevent the image garbage collected.
            canvas.create_image((0, 0), image=ph, anchor='nw')

            text_label = interface_items.get('text_similarity_2')
            text_label.config(text=f"Text similarity: {round(score * 100, 2)}%")

        elif index == 4:
            path = get_image(str(id), database)
            resized_image = Image.fromarray(resize_image(path, 10, []))
            ph = ImageTk.PhotoImage(resized_image)
            canvas = interface_items.get('third_highest_text_sim_canvas')
            canvas.image = ph  # to prevent the image garbage collected.
            canvas.create_image((0, 0), image=ph, anchor='nw')

            text_label = interface_items.get('text_similarity_3')
            text_label.config(text=f"Text similarity: {round(score * 100, 2)}%")
    elif classification == 'color':
        if index == 0:
            path = get_image(str(id), database)
            resized_image = Image.fromarray(resize_image(path, 10, []))
            ph = ImageTk.PhotoImage(resized_image)
            canvas = interface_items.get('highest_colour_sim_canvas')
            canvas.image = ph  # to prevent the image garbage collected.
            canvas.create_image((0, 0), image=ph, anchor='nw')

            text_label = interface_items.get('colour_similarity_1')
            text_label.config(text=f"Colour similarity: {round(score * 100, 2)}%")

        elif index == 2:
            path = get_image(str(id), database)
            resized_image = Image.fromarray(resize_image(path, 10, []))
            ph = ImageTk.PhotoImage(resized_image)
            canvas = interface_items.get('second_highest_colour_sim_canvas')
            canvas.image = ph  # to prevent the image garbage collected.
            canvas.create_image((0, 0), image=ph, anchor='nw')

            text_label = interface_items.get('colour_similarity_2')
            text_label.config(text=f"Colour similarity: {round(score * 100, 2)}%")

        elif index == 4:
            path = get_image(str(id), database)
            resized_image = Image.fromarray(resize_image(path, 10, []))
            ph = ImageTk.PhotoImage(resized_image)
            canvas = interface_items.get('third_highest_colour_sim_canvas')
            canvas.image = ph  # to prevent the image garbage collected.
            canvas.create_image((0, 0), image=ph, anchor='nw')

            text_label = interface_items.get('colour_similarity_3')
            text_label.config(text=f"Colour similarity: {round(score * 100, 2)}%")


#initialise_tkinter()