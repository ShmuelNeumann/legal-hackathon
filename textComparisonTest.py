from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

try:
    while True:

        # Two lists of sentences
        sentences1 = [str(input("\n\nEnter first text\n"))]

        sentences2 = [str(input("Enter second text\n"))]

        #Compute embedding for both lists
        embeddings1 = model.encode(sentences1, convert_to_tensor=True)
        embeddings2 = model.encode(sentences2, convert_to_tensor=True)

        #Compute cosine-similarits
        cosine_scores = util.cos_sim(embeddings1, embeddings2)

        #Output the pairs with their score
        for i in range(len(sentences1)):
            print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))
except KeyboardInterrupt:
    quit()