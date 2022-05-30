

#### Functions

# function for processing the 3 main pieces that make up an image, colour, shape, and text.


def compare_image_shape(database, filepath: str):

    imageDatabase = list(filter(lambda entry: entry.imagePath != 'None', database))

    print("\n====\nInitialising Image Shape ML Algorithm\n====\n")
    model = mlFunctions.init_shape_image_compare()

    comparisonResults = {}

    for index in range(len(imageDatabase)):
        print(f'Comparing image {index+1} out of {len(imageDatabase)}')

        databaseImageEmbedding = mlFunctions.encode_image_shape(model, imageDatabase[index].imagePath)
        imageEmbedding = mlFunctions.encode_image_shape(model, filepath)


        comparisonResults[imageDatabase[index].number] = float(mlFunctions.compare_embeddings(databaseImageEmbedding, imageEmbedding))

    results = getHighestOfDict(comparisonResults, 3)

    return results

def compare_image_text(database, text: str):

    imageDatabase = list(filter(lambda entry: entry.imagePath != 'None', database))

    print("\n====\nInitialising Image Text ML Algorithm\n====\n")
    model = mlFunctions.init_text_encoding()

    comparisonResults = {}

    for index in range(len(imageDatabase)):
        print(f'Comparing image {index+1} out of {len(imageDatabase)}')

        databaseImageEmbedding = mlFunctions.encode_text(model, imageDatabase[index].words)
        imageEmbedding = mlFunctions.encode_text(model, text)


        comparisonResults[imageDatabase[index].number] = float(mlFunctions.compare_embeddings(databaseImageEmbedding, imageEmbedding))

    results = getHighestOfDict(comparisonResults, 3)

    return results

def compare_image_colour(database, filepath: str):

    imageDatabase = list(filter(lambda entry: entry.imagePath != 'None', database))

    print("\n====\nInitialising Image Colour ML Algorithm\n====\n")
    imageData = mlFunctions.preproccess_image_colours(filepath, 5)

    comparisonResults = {}

    for index in range(len(imageDatabase)):
        print(f'Comparing image {index+1} out of {len(imageDatabase)}')

        databaseImageColourData = string_to_lists(imageDatabase[index].colourData)
        


        comparisonResults[int(imageDatabase[index].number)] = mlFunctions.compare_colours(imageData, databaseImageColourData)

    results = getHighestOfDict(comparisonResults, 3)

    return results

def getHighestOfDict(inputDict:dict, numberOfHighest):
    
    outputKeys = []

    for _ in range(numberOfHighest):
    
        highestKey = max(inputDict, key=inputDict.get)
        highestValue = inputDict[highestKey]
        outputKeys.append([int(highestKey), highestValue])
        inputDict.pop(highestKey)

    return outputKeys
    
def string_to_lists(input_string: str) -> list:
    individual_lists = []
    output_list = []
    string_to_manipulate = input_string
    num_closed_bracket = string_to_manipulate.count("]")

    for closed_bracket in range(1,num_closed_bracket):
        if string_to_manipulate[0] == ',':
            string_to_manipulate = string_to_manipulate[1:]
        index_of_closed_bracket = string_to_manipulate.index(']') + 1
        aList = string_to_manipulate[0:index_of_closed_bracket].replace(" ", "")
        if aList[0] == '[' and aList[1] == '[':
            aList = aList[1:]
        individual_lists.append(aList)
        string_to_manipulate = string_to_manipulate[index_of_closed_bracket+1:]


    for string_list in individual_lists:
        inner_list = []
        string_numbers = string_list[1:-1]
        list_of_indiv_numbers = string_numbers.split(",")
        for number in list_of_indiv_numbers:
            inner_list.append(float(number))
        output_list.append(inner_list)

    return output_list


#### Main Program ####


print("\n====\nSearching for Preprocessed Database\n====\n")

import database

#Check if the database needs to be indexed
if database.checkDatabaseIndexing() == False:
    #Index the database
    print("\n====\nNo Preprocessed Database found\nPreprocessing Database\n====\n")
    database.indexDatabase()
    print("\n====\nPreprocessing Complete\n====\n")

import gui

print("\n====\nAccessing Database\n====\n")

database = database.read_database(database.databaseToSaveLocation)

print("\n====\nWaiting for User Input\n====\n")

# Have the user input the image/text
guiData = gui.initialise_tkinter()

comparisonDetails = gui.getInput(guiData) #WIP - This is the function to get [isImage, text, image path]
print("hello")
print("\n====\nInitialising ML functions\n====\n")
import mlFunctions


# If the comparison is an image one, compare the images
if comparisonDetails[0] == True:

    
    shapeResults = compare_image_shape(database, comparisonDetails[1])
    print(shapeResults)

    colourResults = compare_image_colour(database, comparisonDetails[1])
    print(colourResults)

    textResults = compare_image_text(database, comparisonDetails[2])
    print(textResults)

else:
    text


