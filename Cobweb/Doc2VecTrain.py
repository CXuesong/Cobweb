import logging
from gensim.models import doc2vec

def read_corpus(fname, tokens_only=False):
    with open(fname, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line: continue
            tokens = line.split()
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield doc2vec.TaggedDocument(tokens, [i])

def train(inputPath: str, outputPath: str):
    model = doc2vec.Doc2Vec(size=512, min_count=2, iter=55, workers=8)
    logging.info("build_vocab")
    model.build_vocab(read_corpus(inputPath))
    logging.info("train")
    model.train(read_corpus(inputPath), total_examples=model.corpus_count, epochs=model.iter)
    logging.info("save")
    model.save(outputPath)

if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', level=logging.INFO)
    train("bopfulltext-jb-tok-nsw.txt", "doc2vec-model.bin")