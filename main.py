import mlFunctions
import tkinter

import gui



#### Functions

# function for processing the 3 main pieces that make up an image, colour, shape, and text.


def compare_image_shape(database, filepath: str, shapeModel):

    print("\n====\nRunning Image Shape ML Algorithm\n====\n")

    imageDatabase = list(filter(lambda entry: entry.imagePath != 'None', database))

    comparisonResults = {}
    imageEmbedding = mlFunctions.encode_image_shape(shapeModel, filepath)

    for index in range(len(imageDatabase)):
        print(f'Comparing image {index+1} out of {len(imageDatabase)}')

        databaseImageEmbedding = mlFunctions.encode_image_shape(shapeModel, imageDatabase[index].imagePath)


        comparisonResults[imageDatabase[index].number] = float(mlFunctions.compare_embeddings(databaseImageEmbedding, imageEmbedding))

    results = getHighestOfDict(comparisonResults, 3)

    return results

def compare_text(database, text: str, textModel):

    print("\n====\nRunning Text Comparison ML Algorithm\n====\n")

    comparisonResults = {}
    imageEmbedding = mlFunctions.encode_text(textModel, text)

    for index in range(len(database)):
        print(f'Comparing text {index+1} out of {len(database)}')

        databaseImageEmbedding = mlFunctions.encode_text(textModel, database[index].words)


        comparisonResults[database[index].number] = float(mlFunctions.compare_embeddings(databaseImageEmbedding, imageEmbedding))

    results = getHighestOfDict(comparisonResults, 3)

    return results

def compare_image_text(database, text: str, textModel):

    print("\n====\nRunning Text Comparison ML Algorithm\n====\n")

    imageDatabase = list(filter(lambda entry: entry.imagePath != 'None', database))

    comparisonResults = {}
    imageEmbedding = mlFunctions.encode_text(textModel, text)

    for index in range(len(imageDatabase)):
        print(f'Comparing image {index+1} out of {len(imageDatabase)}')

        databaseImageEmbedding = mlFunctions.encode_text(textModel, imageDatabase[index].words)


        comparisonResults[imageDatabase[index].number] = float(mlFunctions.compare_embeddings(databaseImageEmbedding, imageEmbedding))

    results = getHighestOfDict(comparisonResults, 3)

    return results

def compare_image_colour(database, filepath: str):

    imageDatabase = list(filter(lambda entry: entry.imagePath != 'None', database))

    print("\n====\nRunning Image Colour ML Algorithm\n====\n")
    imageData = mlFunctions.preproccess_image_colours(filepath, 5)

    comparisonResults = {}

    for index in range(len(imageDatabase)):
        print(f'Comparing image {index+1} out of {len(imageDatabase)}')

        databaseImageColourData = string_to_lists(imageDatabase[index].colourData)
        
        if len(databaseImageColourData) == 0:
            
            continue


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

def get_results_string(isImage, results, database):

    if isImage == True:
        outputString = "\n====\nRESULTS\n====\n"

        outputString += "\nSimilarities To Other Layouts\n\n"
        for index in range(3):
            outputString += f'{index+1}. Trademark No {results[0][index][0]} has a similarity of {results[0][index][1]} out of 1\n\tMore details can be found at: https://search.ipaustralia.gov.au/trademarks/search/view/{results[0][index][0]}/details' + '\n\n'
        
        outputString += "\nSimilarities To Other Colours\n\n"
        for index in range(3):
            outputString += f'{index+1}. Trademark No {results[1][index][0]} has a similarity of {results[1][index][1]} out of 1\n\tMore details can be found at: https://search.ipaustralia.gov.au/trademarks/search/view/{results[1][index][0]}/details' + '\n\n'
        
        outputString += "\nSimilarities To Other Texts\n\n"
        for index in range(3):
            outputString += f'{index+1}. Trademark No {results[2][index][0]} has a similarity of {results[2][index][1]} out of 1\n\tMore details can be found at: https://search.ipaustralia.gov.au/trademarks/search/view/{results[2][index][0]}/details' + '\n\n'
        return outputString
    
    elif not isImage:
        outputString = "\n====\nRESULTS\n====\n"


        outputString += "\nSimilarities To Other Texts\n\n"
        for index in range(3):
            outputString += f'{index+1}. Trademark No {results[0][index][0]} has a similarity of {results[0][index][1]} out of 1\n\tMore details can be found at: https://search.ipaustralia.gov.au/trademarks/search/view/{results[0][index][0]}/details' + '\n\n'
        
        return outputString

def get_image(number:str, database)->str:
    for index in range(len(database)):
        if database[index].number == str(number):
            return database[index].imagePath

def showNegativeRecomendation(type, number):

    print(f'The {type} is too similar to Trademark No {number}.\n It is recommended to change the image {type}\n\n')


def main():

    print("\n====\nInitialising Program\n====\n")

    print("\n====\nInitialising Image Shape ML Algorithm\n====\n")
    shapeModel = mlFunctions.init_shape_image_compare()
    print("\n====\nInitialising Text ML Algorithm\n====\n")
    textModel = mlFunctions.init_text_encoding()

    input('Press enter to begin:')

    
    #### Main Program ####


    print("\n====\nSearching for Preprocessed Database\n====\n")
    import database


    #Check if the database needs to be indexed
    if database.checkDatabaseIndexing() == False:
        #Index the database
        print("\n====\nNo Preprocessed Database found\nPreprocessing Database\n====\n")
        database.indexDatabase()
        print("\n====\nPreprocessing Complete\n====\n")

    

    print("\n====\nAccessing Database\n====\n")

    database = database.read_database(database.databaseToSaveLocation)

    print("\n====\nWaiting for User Input\n====\n")

    # Have the user input the image/text
    guiData = gui.initialise_tkinter()

    comparisonDetails = gui.getInput(guiData) #WIP - This is the function to get [isImage, text, image path]

    # If the comparison is an image one, compare the images
    if comparisonDetails[0] == True:

        
        shapeResults = compare_image_shape(database, comparisonDetails[1], shapeModel)

        colourResults = compare_image_colour(database, comparisonDetails[1])

        textResults = compare_image_text(database, comparisonDetails[2], textModel)
        
        results_string = get_results_string(True, [shapeResults, colourResults, textResults], database)

        print(results_string)

        colourThreshold = 0.99
        layoutThreshold = 0.6
        textThreshold = 0.2
        neg = False
        
        if colourResults[0][1] > colourThreshold or shapeResults[0][1] > layoutThreshold or textResults[0][1] > textThreshold:
            print(f'\n\n====\nRecommendation\n====\n\nThis Trademark Image will most likely not be filed, for the following reasons:\n\n')
            neg = True

        if shapeResults[0][1] > layoutThreshold:
            showNegativeRecomendation('shape', shapeResults[0][0])


        if colourResults[0][1] > colourThreshold:
            showNegativeRecomendation('colour', colourResults[0][0])



        if textResults[0][1] > textThreshold:
            showNegativeRecomendation('text', textResults[0][0])

        if neg == False:
            print(f'\n\n====\nRecommendation\n====\n\nThis Trademark Image will most likely be filed.\n\n')

            

        gui.show_results(tkinter, True, [shapeResults, colourResults, textResults], database)


    else:
        textResults = compare_text(database, comparisonDetails[2], textModel)

        results_string = get_results_string(False, [textResults], database)
        print(results_string)

        textThreshold = 0.2

        if textResults[0][1] > textThreshold:
            print(f'\n\n====\nRecommendation\n====\n\nThis Trademark Image will most likely not be filed, fot the following reasons:\n\n')
            showNegativeRecomendation('text', textResults[0][1])
        else:
            print(f'\n\n====\nRecommendation\n====\n\nThis Trademark Image will most likely be filed.\n\n')

        gui.show_results(tkinter, False, [textResults], database)

#(data_dict, isImage, [[[number, score], [number, score], [number, score]],  [],   []])
if __name__ == '__main__':
    main()


