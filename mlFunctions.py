from sentence_transformers import SentenceTransformer, util
from PIL import Image

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
from copy import deepcopy
from math import sqrt
#### General Functions ####

def compare_embeddings(embeddings1, embeddings2) -> float:
    """
        Description:
            This function takes two embeddings are compares them.
        Inputs:
            embeddings1: The first embedding list, which should be the output of the function encode_text or encode_image_shape.
            embeddings2: The second embedding list, which should be the output of the function encode_text or encode_image_shape.
        Output:
            A rounded float from 0.0-1.0, which represents the probability of similarity. 1 is most similar, 0 is most different.
    """

    #Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)


    output = cosine_scores[0][0]

    return output

#### Text Compare Functions ####

def init_text_encoding():
    """
        Description:
            The function returns the ML model. Note that this function can take a long time to run.
        Inputs:
            NA
        Output:
            The ML model.
    """
    return SentenceTransformer('all-mpnet-base-v2')

def encode_text(model, text):
    """
        Description:
            This function takes encodes a text into embeddings, using the specified model.
        Inputs:
            model: The ML model to use, sshould be the output from init_text_encoding.
            text: The sentance to encode, as a string
        Output:
            The embedded data, in the form of a list of tensors.
    """
    
    #Convert the text to a list
    sentences1 = [text]

    # Encode the text using the specified model
    embeddings = model.encode(sentences1, convert_to_tensor=True)

    return embeddings

def run_text_compare():

    # This is a sample of how to compare texts.

    model = init_text_encoding()

    try:
        while True:
            text1 = input("\nEnter the first text:\n")
            text2 = input("Enter the second text:\n")

            encoding1 = encode_text(model, text1)
            encoding2 = encode_text(model, text2)
              
            similarity = compare_embeddings(encoding1, encoding2)

            print(f'Similarity: {similarity}')

    except KeyboardInterrupt:
        quit()

#### Image Shape Compare ####

def init_shape_image_compare():
    """
        Description:
            The function to return the ML model. Note that this function can take a long time to run.
        Inputs:
            NA
        Output:
            The ML model.
    """
    return SentenceTransformer('clip-ViT-B-32')

def encode_image_shape(model, path):
    """
        Description:
            This function takes encodes an image into embeddings, using the specified model.
        Inputs:
            model: The ML model to use, sshould be the output from init_image_encoding.
            path: The path of the image to encode, as a string
        Output:
            The embedded data, in the form of a list of tensors.
    """

    # Encode the text using the specified model
    embeddings = model.encode(Image.open(path))

    return embeddings

def run_image_shape_compare():

    # This is a sample of how to compare two images.

    path1 = r'C:\Users\sammy.LAPTOP-RUR693FV\OneDrive - Monash University\ML_tests\blue.jpg'
    path2 = r'C:\Users\sammy.LAPTOP-RUR693FV\OneDrive - Monash University\ML_tests\green.jpg'

    model = init_shape_image_compare()

    encoding1 = encode_image_shape(model, path1)
    encoding2 = encode_image_shape(model, path2)
    
    similarity = compare_embeddings(encoding1, encoding2)

    print(f'Similarity: {similarity}')

#### Image Colour Compare ####

def RGB2HEX(colour:list)->str:
    """
        Description:
            This function converts rgb values to the hexidecimal codes
        Inputs:
            colour: A lsit of three float, representing red, green and blue.
        Output:
            A string with the hexidecimal code for the colour.
    """
    return "#{:02x}{:02x}{:02x}".format(int(colour[0]), int(colour[1]), int(colour[2]))

def get_image(image_path: str):
    """
        Description:
            This function gets an image based on a patha nd colour corrects it.
        Inputs:
            image_path: A raw string with the image path
        Output:
            The image object
    """

    image = cv2.imread(image_path)
    #This line converts the image from BGR to RGB values
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image

def get_colours(image, number_of_colours: int, show_chart: bool)->list:
    """
        Description:
            This function gets the the most common colours of an image using K-means clustering, and encodes it into data format.
        Inputs:
            image: The image to analyze, should be the output from get_image
            number_of_colours: The number of colours to divide the iamge into, as an integer.
            show_chart: A bool that indicates if a pie graph of the colours should be displayed.
        Output:
            The colour data, in the form of a list of colour dictionaries. Each of the dictionaries contain the number of pixel that fall into that colour, along with the rgb and hex values of the colour.
    """

    # We first resize the image
    modified_image = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)

    # Runt the K-means algorithm. labels holds the array (?) output
    clf = KMeans(n_clusters = number_of_colours, random_state=0)
    labels = clf.fit_predict(modified_image)
    counts = Counter(labels)
    #This line gets the centre of the clusters of colours
    center_colours = clf.cluster_centers_

    # We get the rgb and hex values of the colours as a list
    ordered_colours = [center_colours[i] for i in counts.keys()]
    hex_colours = [RGB2HEX(ordered_colours[i]) for i in counts.keys()]
    rgb_colours = [ordered_colours[i] for i in counts.keys()]

    #This code displays the pie chart, if required.
    if (show_chart):
        plt.figure(figsize=(8,6))
        plt.pie(counts.values(), labels = hex_colours, colors = hex_colours)
        plt.show()
    
    # This wil be our output list
    colour_stats = []

    #For each f the colours, we create a dictionary to hold their data.
    for i in counts.keys():
        colour_stat = {}
        colour_stat['rgb'] = list(rgb_colours[i]) #What are the rgb values (list of floats)
        colour_stat['value'] = counts[i] #how many pixels are in the cluster (int)
        colour_stat['hex'] = hex_colours[i] # WHat is the hex code of the colour (str)
        colour_stats.append(colour_stat)


    return colour_stats

def not_white_or_black(colour: list) -> bool:
    """
        Description:
            This function checks if a colour is similar to black or white.
        Inputs:
            colour: A list of red, blue, green floats
        Output:
            True if the colour is not close to Black or White, False if it is.
    """

    if colour[0] > 200 and colour[1] > 240 and colour[2] > 200:
        return False
    elif colour[0] < 50 and colour[1] < 50 and colour[2] < 50:
        return False
    else:
        return True

def remove_shades(colourData: list, show_chart: bool)->list:
    """
        Description:
            This function gets the colour data of a image and removes any colours similar to black or white.
        Inputs:
            colourData: a list of colour dictionaries, should be from get_colours().
            show_chart: A bool representing if a pie graph shuld be displayed.
        Output:
            The updated colourData.
    """

    #This filter removes any colours that done return true from the not_white_or_black() function
    modified_data = list(filter(lambda colour : not_white_or_black(colour['rgb']), colourData))

    # display the pie chart, if required
    if (show_chart):
        plt.figure(figsize=(8,6))

        values = [colour['value'] for colour in modified_data]
        hexs = [colour['hex'] for colour in modified_data]

        plt.pie(values, labels= hexs, colors= hexs)
        plt.show()

    return modified_data

def weigh_data(data: list)->list:
    """
        Description:
            This function gets the colour data of a image and scales the rgb values by how common the colour is.
            Note that data IS NOT MUTATED.
        Inputs:
            colourData: a list of colour dictionaries, should be from get_colours().
        Output:
            A new weighted colourData.
    """

    #First we find the total number of pixels in the colour clusters
    total_values = 0

    values = [dataEntry['value'] for dataEntry in data]

    for value in values:
        total_values += value
    
    # Turn the numbers of pixels in the cluster into a float from 0-1
    weightedValues = list(map(lambda value: value/total_values, values))

    weightedData = deepcopy(data)


    #For each colour, multiply each of the rgb values by the proportion of pixels in the image.
    for index in range(len(data)):
    
        rgb = list(map(lambda value: value * weightedValues[index], weightedData[index]['rgb']))
        weightedData[index] = rgb


    return weightedData

def distance_between_points(point1:list, point2:list)->float:
    """
        Description:
            This function returns the distance between two points in 3d space.
        Inputs:
            point1: a list of of floats representing the x, y, z values of the first point.
            point2: a list of of floats representing the x, y, z values of the second point.
        Output:
            The  distance between the two points as a float.
    """
    return sqrt(((point1[0] - point2[0])**2) + ((point1[1] - point2[1])**2) + ((point1[2] - point2[2])**2))

def average(lst:list)->float:
    """
        Description:
            This function returns the average value of a list of floats.
        Inputs:
            lst: A list of floats
        Output:
            The  average of the lst values, as a float.
    """
    
    total = 0

    for i in lst:
        total += i
    
    return total/len(lst)

def find_centre_of_points(points:list)->list:
    """
        Description:
            This function returns the center point of a list of points in 3d space.
        Inputs:
            points: A list of lists, each sublist containing float representing x,y,z values.
        Output:
            The average point, in the form of a list of x,y,z floats.
    """

    #We fist get all the values of the points.
    xValues = []
    yValues = []
    zValues = []
    
    for point in points:
        xValues.append(point[0])
        yValues.append(point[1])
        zValues.append(point[2])
    
    #Find the average x value, average y value, and average z value
    xAverage = average(xValues)
    yAverage = average(yValues)
    zAverage = average(zValues)

    return [xAverage, yAverage, zAverage]

def compare_colours(data1:list, data2:list) -> float:
    """
        Description:
            This function returns the distance betwene two colour datas
        Inputs:
            data1: The first list of dictionaries representing an image's weighted colours, should be from preproccess_image_colours()
            data2: The second list of dictionaries representing an image's weighted colours, should be from preproccess_image_colours()        
        Output:
            The difference between the colours of an image, as a float.
                <1: identical
                ~10: very similar
                ~30: average
                ~50: very different

    """
    centerOfData1 = find_centre_of_points(data1)
    centerOfData2 = find_centre_of_points(data2)

    diff = distance_between_points(centerOfData1, centerOfData2)

    return diff

def preproccess_image_colours(path:str, noColoursToDetect:int)->list:
    """
        Description:
            This function converts an image to colour data
        Inputs:
            path: The string representing the image path.
            noColoursToDetect: The number of colours, as an int, to divide the image into, before proccessing.
        Output:
            The coluor data as a list of weighted colour lists of rgb values.
    """

    #Get the image
    image = get_image(path)
    
    #Extract the colours
    colourData = get_colours(image, noColoursToDetect, False)

    #Remove whites and blacks
    cleanedColourData = remove_shades(colourData, True)

    #Weigh the rgb values
    weightedData = weigh_data(cleanedColourData)

    return weightedData

def run_image_colour_compare():
    #A sampl of comparing two image's colours

    path1 = r'C:\Users\sammy.LAPTOP-RUR693FV\OneDrive - Monash University\ML_tests\blue.jpg'
    path2 = r'C:\Users\sammy.LAPTOP-RUR693FV\OneDrive - Monash University\ML_tests\green.jpg'
    
    
    data1 = preproccess_image_colours(path1, 5)
    data2 = preproccess_image_colours(path2, 5)

    difference = compare_colours(data1, data2)

    return difference

#### Testing ####

if __name__ == '__main__':

    #Samples
    print(run_image_colour_compare())
    print(run_image_shape_compare())
    print(run_text_compare())