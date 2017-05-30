import logging
from gensim.models import word2vec

def train(inputPath: str, outputPath: str):
    logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', level=logging.INFO)
    corpus = word2vec.Text8Corpus("zhcnwp-tok.txt")
    model = word2vec.Word2Vec(corpus, size=256, window=8, workers=30)
    model.save(outputPath)
    
if __name__ == "__main__":
    train("zhcnwp-tok.txt", "zhcnwp-model.bin")