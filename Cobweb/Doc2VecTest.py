import logging
from gensim.models import doc2vec

def test(modelPath: str):
    logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', level=logging.INFO)
    model = doc2vec.Doc2Vec.load(modelPath)
    print(model.infer_vector(["电容器", "的", "基本", "特性"]))

if __name__ == "__main__":
    test("doc2vec-model.bin")