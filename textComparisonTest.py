from sentence_transformers import SentenceTransformer, util
from PIL import Image

#Load CLIP model
model = SentenceTransformer('clip-ViT-B-32')

#Encode an image:
img_emb = model.encode(Image.open(r'C:\Users\sammy.LAPTOP-RUR693FV\Pictures\Picture1.jpg'))

#Encode text descriptions
img_emb_2 = model.encode(Image.open(r'C:\Users\sammy.LAPTOP-RUR693FV\Pictures\Picture3.jpg'))

#Compute cosine similarities 
cos_scores = util.cos_sim(img_emb, img_emb_2)
print(cos_scores)