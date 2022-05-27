import time
from turtle import color

from pandas import array
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
from torch import true_divide

def RGB2HEX(colour):
    return "#{:02x}{:02x}{:02x}".format(int(colour[0]), int(colour[1]), int(colour[2]))

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def get_colours(image, number_of_colours, show_chart):
    modified_image = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)

    clf = KMeans(n_clusters = number_of_colours, random_state=0)
    labels = clf.fit_predict(modified_image)

    counts = Counter(labels)
    center_colours = clf.cluster_centers_

    ordered_colours = []
    hex_colours = []
    rgb_colours = []

    for i in counts.keys():
        if not_white_or_black(center_colours[i]):
            ordered_colours.append(center_colours[i])
            hex_colours.append(RGB2HEX(ordered_colours[i]))
            rgb_colours.append(ordered_colours[i])

    if (show_chart):
        plt.figure(figsize=(8,6))
        plt.pie(counts.values(), colors = hex_colours)
    
    return rgb_colours

def not_white_or_black(colour: color):

    if colour[0] > 240 and colour[1] > 240 and colour[2] > 240:
        return False
    elif colour[0] < 50 and colour[1] < 50 and colour[2] < 50:
        return False
    else:
        return True

def match_image_by_colour(image, colour, threshhold=60, number_of_colours = 10):
    image_colours = get_colours(image, number_of_colours, True)
    plt.show()
    selected_colour = rgb2lab(np.uint(np.asarray([[colour]])))

    select_image = False
    for i in range(number_of_colours):
        curr_colour = rgb2lab(np.uint(np.asarray([[image_colours[i]]])))
        diff = deltaE_cie76(selected_colour, curr_colour)
        if diff < threshhold:
           selected_image = True
    return select_image

def show_selected_images(images, colour, threshold, colours_to_match):
    index = 1

    for i in range(len(images)):
        selected = match_image_by_colour(images[i], colour, threshold, colours_to_match)

        if selected:
            plt. subplot(1,5, index)
            plt.imshow(images[i])
            index+=1

#plt.figure(figsize=(20,10))
#show_selected_images(images, COLORS['BLUE'], 60, 5)

#get_colours(get_image(r'C:\Users\sammy.LAPTOP-RUR693FV\Pictures\image.jpg'), 8, True)

#plt.show()

def compare_image_colours():
    no_of_colours = 2
    
    path_1 = r'C:\Users\sammy.LAPTOP-RUR693FV\Pictures\Picture2.jpg'
    path_2 = r'C:\Users\sammy.LAPTOP-RUR693FV\Pictures\Picture4.jpg'
    
    image_1 = cv2.imread(path_1)
    image_2 = cv2.imread(path_2)

    image_colours_1 = get_colours(image_1, no_of_colours, True)
    plt.show()
    image_colours_2 = get_colours(image_2, no_of_colours, True)
    plt.show()

    total_difference = 0

    for x in range(len(image_colours_1)):
        for y in range(len(image_colours_2)):
            colour_1 = rgb2lab(np.uint(np.asarray([[image_colours_1[x]]])))
            colour_2 = rgb2lab(np.uint(np.asarray([[image_colours_2[y]]])))

            diff = deltaE_cie76(colour_1, colour_2)

            total_difference += abs(diff)
    

    difference = round(float(total_difference * 1e4), 4)


    return difference


print(compare_image_colours())