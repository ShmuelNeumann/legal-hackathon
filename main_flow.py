



#Function Imports
import database
import gui

#### Functions

# function for processing the 3 main pieces that make up an image, colour, shape, and text.
def compare_image(filepath: str, text: str,  database):
    pass

# function for processing the input text.
def compare_text(text: str):
    pass

# button to show the results in a report format after image/text has been processed.
def display_results():
    pass

# run the backbone code here for keeping the interface on and root for all decisions made on interface
def main_flow():
    pass

# not sure if needed but exit the interface done by closing window.
def exit():
    pass


#### Main Program ####

#Check if the database needs to be indexed
if database.checkDatabaseIndexing() == False:
    #Index the database
    print("\n====\nNo indexed Database found\nPreprocessing Database\n====\n")
    database.indexDatabase()
    print("\n====\nIndexing Complete\n====\n")


# Have the user input the image/text
comparisonDetails = gui.getInput() #WIP - This is the function to get [isImage, text, image path]

# Get the database
database = database.read_database(database.databaseToSaveLocation)

# If the comparison is an image one, compare the images
if comparisonDetails[0] == True:
    compare_image()
    



