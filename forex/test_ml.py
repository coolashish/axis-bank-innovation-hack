#!/usr/bin/python
import xgboost as xgb
import pandas as pd

def get_prediction(filename, path):

    colnames = ['countryCount', 'cityCount', 'importCount', 'exportCount', 'keywordCount', 'iec', 'target']
    test = pd.read_csv(filename, header = None, names = colnames)
    target = test['target']
    test = test.drop(['target'], axis = 1)
    dtest = xgb.DMatrix(test.values, target.values)
    bst = xgb.Booster(model_file= path + '/forex/xgb.model')
    pred = bst.predict(dtest)
    return pred

if __name__ == '__main__':
    get_prediction('/home/ashish/codes/axis-bank/demo.test')
