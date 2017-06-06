import logging
from gensim.models import word2vec
import numpy as np
import scipy.io as sio
import scipy.spatial as spatial
import localconfig
import qaExtractor
import itertools
import jieba

def main(modelPath: str, qaPath:str, matPath: str):
    logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', level=logging.INFO)
    model = word2vec.Word2Vec.load(modelPath)
    trainQaList = list(qaEntriesFromFile(model, qaPath))
    def vectorGenerator():
        entryCount = 0
        for qa in trainQaList:
            entryCount += 1
            sim = 1 - spatial.distance.cosine(qa.questionVector, qa.answerVector)
            yield np.hstack((qa.questionVector, qa.answerVector, sim))
    trainX = np.vstack(vectorGenerator())
    trainY = np.vstack((1 if qa.corresponds else 0 for qa in trainQaList))
    sio.savemat(matPath, {"X": trainX, "Y": trainY}, do_compression=True)

def qaEntriesFromFile(model, path: str):
    entryCount = 0
    for qa in qaExtractor.entriesFromFile(path):
        entryCount += 1
        #print(entryCount)
        qa.questionVector = model.infer_vector(jieba.cut(qa.question))
        qa.answerVector = model.infer_vector(jieba.cut(qa.answer))
        yield qa
        if entryCount % 10000 == 0: logging.info("已导入：%d条。" % entryCount)

if __name__ == "__main__":
    main("doc2vec-model.bin", localconfig.QaDevDataDir, "qa-dev-d.mat")
    main("doc2vec-model.bin", localconfig.QaTrainDataDir, "qa-train-d.mat")
    main("doc2vec-model.bin", localconfig.QaTestDataDir, "qa-test-d.mat")
