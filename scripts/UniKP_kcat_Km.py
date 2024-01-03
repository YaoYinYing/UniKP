from UniKP.utils import Seq_to_vec, smiles_to_vec

from sklearn.ensemble import ExtraTreesRegressor
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
import pickle
import math




def Kcat_predict(Ifeature, Label):
    kf = KFold(n_splits=5, shuffle=True)
    All_pre_label = []
    All_real_label = []
    for train_index, test_index in kf.split(Ifeature, Label):
        Train_data, Train_label = Ifeature[train_index], Label[train_index]
        Test_data, Test_label = Ifeature[test_index], Label[test_index]
        model = ExtraTreesRegressor()
        model.fit(Train_data, Train_label)
        Pre_label = model.predict(Test_data)
        All_pre_label.extend(Pre_label)
        All_real_label.extend(Test_label)
    res = pd.DataFrame({'Value': All_real_label, 'Predict_Label': All_pre_label})
    res.to_excel('Kcat_Km/Kcat_Km_5_cv.xlsx')


if __name__ == '__main__':
    res = np.array(pd.read_excel('Kcat_Km/kcat_km_samples.xlsx', sheet_name='main')).T
    Smiles = res[1]
    sequences = res[2]
    Value = res[0]
    for i in range(len(Value)):
        Value[i] = math.log(Value[i], 10)
    print(max(Value), min(Value))
    smiles_input = smiles_to_vec(Smiles)
    sequence_input = Seq_to_vec(sequences)
    feature = np.concatenate((smiles_input, sequence_input), axis=1)
    with open("Kcat_Km/Kcat_Km_features_910.pkl", "wb") as f:
        pickle.dump(feature, f)
    feature = np.array(feature)
    Label = np.array(Value)
    Kcat_predict(feature, Label)
