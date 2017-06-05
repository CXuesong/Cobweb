import logging
from gensim.models import word2vec
import numpy as np
import scipy.io as sio
import scipy.spatial as spatial
import localconfig
import qaExtractor
import itertools
import jieba

FORCE_TEST_SET = True

nanFiller = np.empty((256*2+1,))
nanFiller[:] = np.nan

def main(modelPath: str, qaPath:str, matPath: str):
    logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', level=logging.INFO)
    model = word2vec.Word2Vec.load(modelPath)
    trainQaList = list(qaEntriesFromFile(model, qaPath))
    def vectorGenerator():
        entryCount = 0
        for qa in trainQaList:
            entryCount += 1
            if qa.questionVector is None or qa.answerVector is None:
                logging.warn("行：{0}，标记{1}：无问题或答案向量。".format(entryCount, qa.corresponds))
                if FORCE_TEST_SET or qa.corresponds is None:
                    # This is test set
                    yield nanFiller
                continue
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
        qa.questionVector = evalSentenceVector(model, qa.question)
        qa.answerVector = evalSentenceVector(model, qa.answer)
        yield qa
        if entryCount % 10000 == 0: logging.info("已导入：%d条。" % entryCount)

# https://stackoverflow.com/questions/22129943/how-to-calculate-the-sentence-similarity-using-word2vec-model-of-gensim-with-pyt
def evalSentenceVector(model:word2vec.Word2Vec, sentence:str):
    '''Averages all words vectors in a given paragraph.'''
    featureVec = None
    nwords = 0

    #list containing names of words in the vocabulary
    #index2word_set = set(model.index2word) this is moved as input param for performance reasons
    for word in jieba.cut(sentence):
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
    main("zhcnwp-model.bin", localconfig.QaDevDataDir, "qa-dev.mat")
    #main("zhcnwp-model.bin", localconfig.QaTrainDataDir, "qa-train.mat")
    main("zhcnwp-model.bin", localconfig.QaTestDataDir, "qa-test.mat")
