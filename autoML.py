import time

#### Text Compare ####

from sentence_transformers import SentenceTransformer, util

def init_text_compare():
    """
        Description:
            The function to return the ML model. Note that this function can take a long time to run
        Inputs:
            NA
        Output:
            The ML model.
    """
    return SentenceTransformer('all-mpnet-base-v2')

def text_compare(model, text1, text2):
    """
        Description:
            This function compares two texts using NLP embedding, a form of ML.
        Inputs:
            model: The ML model to use, which should be the output of init_Text_Compare.
            text1: The first string to compare.
            text2: the second string to compare.
        Output:
            A rounded float from 0.0-1.0, which represents the probability.
    """
    #convert the two texts to lists
    sentences1 = [text1]
    sentences2 = [text2]


    embeddings1 = model.encode(sentences1, convert_to_tensor=True)
    embeddings2 = model.encode(sentences2, convert_to_tensor=True)

    #Compute cosine-similarits
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    output = float("{:.4}".format(cosine_scores[0][0]))

    return output

def run_text_compare():

    model = init_text_compare()

    try:
        while True:
            text1 = input("\nEnter the first text:\n")
            text2 = input("Enter the second text:\n")

            print(f'Similarity: {text_compare(model, text1, text2)}')

    except KeyboardInterrupt:
        quit()

#### General Image Compare ####

from sentence_transformers import SentenceTransformer, util
from PIL import Image

def init_general_image_compare():
    """
        Description:
            The function to return the ML model. Note that this function can take a long time to run
        Inputs:
            NA
        Output:
            The ML model.
    """
    return SentenceTransformer('clip-ViT-B-32')

def general_image_compare(model, path1, path2):
    """
        Description:
            This function compares two images using a form of ML.
        Inputs:
            model: The ML model to use, which should be the output of init_general_image_compare.
            path1: The first image path, as a raw string, to compare from.
            path2: The second image path, as a raw string, to compare to.
        Output:
            A rounded float from 0.0-1.0, which represents the probability.
    """    
    
    img_emb = model.encode(Image.open(path1))

    #Encode text descriptions
    img_emb_2 = model.encode(Image.open(path2))

    #Compute cosine similarities 
    cos_scores = util.cos_sim(img_emb, img_emb_2)
    
    
    output = float("{:.4}".format(cos_scores[0][0]))

    return output

def run_general_image_compare():

    path1 = r'C:\Users\sammy.LAPTOP-RUR693FV\Pictures\Picture1.jpg'
    path2 = r'C:\Users\sammy.LAPTOP-RUR693FV\Pictures\Picture2.jpg'

    model = init_general_image_compare()

    output = general_image_compare(model, path1, path2)

    print(f'Score: {output}')

#### Colour Identification ####

def identify_colours(path, number_of_colours):
    print(time.time())
    from cv2 import kmeans
    import matplotlib
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import sklearn
    from sklearn.cluster import KMeans
    from collections import Counter
    from skimage.color import rgb2lab, deltaE_cie76
    import cv2

    plt.style.use('ggplot')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.serif'] = 'Ubuntu'
    plt.rcParams['font.monospace'] = 'Ubuntu Mono'
    plt.rcParams['font.size'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['figure.titlesize'] = 12
    plt.rcParams['image.cmap'] = 'jet'
    plt.rcParams['image.interpolation'] = 'none'
    plt.rcParams['figure.figsize'] = (10,10)
    plt.rcParams['axes.grid'] = False
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['lines.markersize'] = 8
    colors = ['xkcd:pale orange', 'xkcd:sea blue', 'xkcd:pale red', 'xkcd:sage green', 'xkcd:terra cotta', 'xkcd:dull purple', 'xkcd:teal', 'xkcd: goldenrod', 'xkcd:cadet blue',
    'xkcd:scarlet']

    def get_image(image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    def RGB2HEX(color):
        return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))
    
    image = get_image(path)
    
    modified_image = image.reshape(image.shape[0]*image.shape[1], 3)
    clf = KMeans(n_clusters=number_of_colours)
    labels = clf.fit_predict(modified_image)

    counts = Counter(labels)

    center_colours = clf.cluster_centers_
    # We get order colours by iterating htorugh the keys
    ordered_colours = [center_colours[i] for i in counts.keys()]
    hex_colours = [RGB2HEX(ordered_colours[i]) for i in counts.keys()]
    rgb_colours = [ordered_colours[i] for i in counts.keys()]

    plt.title('Colour Detection ($n=10$)', fontsize=20)
    plt.pie(counts.values(), labels = hex_colours, colors = hex_colours)
    print(time.time())
    plt.show()
    

def run_colour_identification():
    identify_colours(r'C:\Users\sammy.LAPTOP-RUR693FV\Pictures\Windbound\13_2_2022__19_50_58.png', 5)

#### Testing ####

if __name__ == '__main__':
    run_colour_identification()