import xgboost as xgb
import numpy as np
from scipy.io import loadmat,savemat
import pickle
import matplotlib.pyplot as plt
import pandas as pd

TRAIN_MAT = "qa-dev.mat"
TEST_MAT = "qa-test.mat"
PROBLEM_NAME = "DEV"

print("训练集已经加载。")

def Train() :
    mat = loadmat(TRAIN_MAT, variable_names = ("X", "YA"))
    dtrain = xgb.DMatrix(mat["X"], label=mat["YA"])
    param = {'max_depth':6, 'eta':0.1, 'silent':False, 'objective':'rank:pairwise', 'min_child_weight': 1}
    num_round = 150
    bst = xgb.train(param, dtrain, num_round)
    #xgb.plot_importance(bst)
    PlotFeatureImportances(bst, mat["X"].shape[1])
    plt.savefig("RFeatureImportance-" + PROBLEM_NAME + ".png", transparent=True)
    with open("RModel" + PROBLEM_NAME + ".pkl", "wb") as fs :
        pickle.dump(bst, fs)

def Predict() :
    mat = loadmat(TEST_MAT, variable_names=("X", "XL"))
    dtest = xgb.DMatrix(mat["X"])
    print("测试集已经加载。")

    with open("RModel" + PROBLEM_NAME + ".pkl", "rb") as fs :
        bst = pickle.load(fs)
    print("模型已经加载。")

    # make prediction
    Y = bst.predict(dtest)

    # 用于故障排查
    savemat("Predicted" + PROBLEM_NAME + ".mat", {"X": mat["X"], "XL": mat["XL"], "Y": Y},
            appendmat=False, do_compression=True)

    df = pd.DataFrame({"XL": mat["XL"].reshape(-1),  "Y": Y.reshape(-1)})
    df.sort_values(by="Y", ascending=False, inplace=True)

    with open("Result" + PROBLEM_NAME + ".txt", "w") as ofs, \
        open("ResultV" + PROBLEM_NAME + ".txt", "w") as ofsv:
        for row in df.itertuples() :
            ofs.write("{0:010d}".format(row.XL))
            ofs.write("\n")
            ofsv.write("{0:010d}\t{1}".format(row.XL, row.Y))
            ofsv.write("\n")

def CV() :
    mat = loadmat(TRAIN_MAT, variable_names = ("X", "Y"))
    dtrain = xgb.DMatrix(mat["X"], label=mat["Y"])
    param = {'max_depth':6, 'eta':0.1, 'silent':True, 'objective':'rank:pairwise', 'min_child_weight': 1}
    num_round = 150
    rec = {}
    xgb.cv(param, dtrain, num_round, nfold=5,
       metrics={'map'}, seed = 0,
       callbacks=[xgb.callback.print_evaluation(show_stdv=False)])
    print(rec)

def PlotFeatureImportances(reg, Xdim, title=None) :
    plt.figure(figsize = (12, 6))
    fi = MlUtility.xgbFeatureImportances(reg, Xdim)
    plt.bar(range(0, len(fi)), fi)
    plt.xticks(range(0, len(fi), 5))
    plt.title(title)
    plt.grid()

#Train()
#Predict()
CV()