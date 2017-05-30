import logging
from gensim.models import word2vec
import numpy as np
import scipy.io as sio
import localconfig
import qaExtractor
import itertools

def main(modelPath: str, matPath: str):
    logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', level=logging.INFO)
    model = word2vec.Word2Vec.load(modelPath)
    trainQaList = list(qaEntriesFromFile(model, localconfig.QaDevDataDir))
    trainX = np.vstack((np.hstack((qa.questionVector, qa.answerVector)) for qa in trainQaList))
    trainY = np.vstack((1 if qa.corresponds else 0 for qa in trainQaList))
    sio.savemat(matPath, {"X": trainX, "Y": trainY}, do_compression=True)

def qaEntriesFromFile(model, path: str):
    entryCount = 0
    for qa in qaExtractor.entriesFromFile(path):
        entryCount += 1
        qa.questionVector = evalSentenceVector(model, qa.question)
        qa.answerVector = evalSentenceVector(model, qa.answer)
        if qa.questionVector is None or qa.answerVector is None:
            logging.warn("行：%d，无问题或答案向量。" % entryCount)
        else:
            yield qa
        if entryCount % 10000 == 0: logging.info("已导入：%d条。" % entryCount)

# https://stackoverflow.com/questions/22129943/how-to-calculate-the-sentence-similarity-using-word2vec-model-of-gensim-with-pyt
def evalSentenceVector(model:word2vec.Word2Vec, sentence:str):
    '''Averages all words vectors in a given paragraph.'''
    featureVec = None
    nwords = 0

    #list containing names of words in the vocabulary
    #index2word_set = set(model.index2word) this is moved as input param for performance reasons
    for word in sentence:
        try:
            vec = model[word]
        except KeyError:
            continue
        nwords += 1
        if featureVec is None:
            featureVec = vec
        else:
            featureVec = np.add(featureVec, vec)

    if(nwords > 0):
        featureVec = np.divide(featureVec, nwords)
    return featureVec

if __name__ == "__main__":
    main("zhcnwp-model.bin", "qa-dev.mat")
