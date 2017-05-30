import logging
from gensim.models import word2vec

def test(modelPath: str):
    logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', level=logging.INFO)
    model = word2vec.Word2Vec.load(modelPath)
    print(model.wv.most_similar(positive="想"))

if __name__ == "__main__":
    test("zhcnwp-model.bin")