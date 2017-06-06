import xgboost as xgb
import numpy as np
from scipy.io import loadmat,savemat
import pickle
import matplotlib.pyplot as plt

TRAIN_MAT = "qa-train.mat"
#TEST_MAT = "qa-test.mat"
TEST_MAT = "qa-dev.mat"
PROBLEM_NAME = "TRAIN"

print("训练集已经加载。")

def Train() :
    mat = loadmat(TRAIN_MAT, variable_names = ("X", "Y"))
    dtrain = xgb.DMatrix(mat["X"], label=mat["Y"])
    param = {'max_depth':6, 'eta':0.1, 'silent':False, 'objective':'rank:pairwise', 'min_child_weight': 1}
    num_round = 120
    bst = xgb.train(param, dtrain, num_round)
    xgb.plot_importance(bst)
    plt.savefig("RFeatureImportance-" + PROBLEM_NAME + ".png", transparent=True)
    with open("RModel" + PROBLEM_NAME + ".pkl", "wb") as fs :
        pickle.dump(bst, fs)

def Predict() :
    mat = loadmat(TEST_MAT, variable_names=("X",))
    X = mat["X"]
    dtest = xgb.DMatrix(X)
    print("测试集已经加载。")

    with open("RModel" + PROBLEM_NAME + ".pkl", "rb") as fs:
        bst = pickle.load(fs)
    print("模型已经加载。")

    # make prediction
    Y = bst.predict(dtest)

    with open("Result" + PROBLEM_NAME + ".txt", "w") as ofs:
        for i in range(0, Y.shape[0]):
            value = Y[i]
            if np.isnan(X[i][0]): value = -100
            value = np.exp(value)
            ofs.write("{0}".format(value))
            ofs.write("\n")

def CV() :
    mat = loadmat(TRAIN_MAT, variable_names = ("X", "Y"))
    dtrain = xgb.DMatrix(mat["X"], label=mat["Y"])
    param = {'max_depth':6, 'eta':0.1, 'silent':True, 'objective':'rank:pairwise', 'min_child_weight': 1}
    num_round = 100
    rec = {}
    xgb.cv(param, dtrain, num_round, nfold=5,
       metrics={'map'}, seed = 0,
       callbacks=[xgb.callback.print_evaluation(show_stdv=False)])
    print(rec)

Train()
Predict()
#CV()