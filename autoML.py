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
    return SentenceTransformer('clip-ViT-B-32')

def general_image_compare(model, path1, path2):
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

#### Testing ####

if __name__ == '__main__':
    run_general_image_compare()