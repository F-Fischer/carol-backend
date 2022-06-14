import pandas as pd
import numpy as np
from jarowinkler import jarowinkler_similarity

def get_dataframe():
    df = pd.read_csv("data/medicamentos.csv", sep=';', encoding='latin-1')
    return df

def get_prob_value(target,columna,thr,droga):
    med = get_dataframe()
    sims =[]
    method= jarowinkler_similarity
    if droga != "error":
        vocab= list(set(med[med['Principio activo']==droga][columna]))
    else:
        vocab= list(set(med[columna]))

    for word in vocab:
        sims.append(method(target, word))
    if np.max(sims) > thr:
        return vocab[np.argmax(sims)] ,np.max(sims)
    else:
        return "error" , 0

def predict(target):
    med = get_dataframe()
    droga_list = []
    gramaje_list = []
    unidad_list =[]
    final_list = []
    for w in target:
        droga_pred=get_prob_value(w.lower() ,'Principio activo',0.81,"error")
        if droga_pred[0] != "error":
            droga_list.append(droga_pred)
    if len(droga_list)==0:
        droga_select = "error"
    else:
        droga_select=max(droga_list,key=lambda item:item[1])[0]

    if droga_select != "error":
        final_list.append(droga_select)

        for w in target:
            gramaje_pred= get_prob_value(w.lower(),'Potencia',0.7,droga_select)
            if gramaje_pred[0] != "error":
                gramaje_list.append(gramaje_pred)

        if len(gramaje_list)==0:
            gramaje_select = "error"
        else:
            gramaje_select=max(gramaje_list,key=lambda item:item[1])[0]

        if gramaje_select != "error":
            final_list.append(gramaje_select)

#            for w in target:
#                unidad_pred= get_prob_value(w.lower(),'Unidad de potencia',0.7,droga_select)
#                if unidad_pred[0] != "error":
#                    unidad_list.append(unidad_pred)
#
#            if len(unidad_list)==0:
#                unidad_select = "error"
#            else:
#                unidad_select=max(unidad_list,key=lambda item:item[1])[0]
#
#            if unidad_select != "error":
#                final_list.append(unidad_select)
#            else:

        if droga_select != "error" and gramaje_select != "error":
                unidad_select=med[(med["Principio activo"]==droga_select)&(med["Potencia"]==gramaje_select)]["Unidad de potencia"].iloc[0]
                final_list.append(unidad_select)

    return final_list
