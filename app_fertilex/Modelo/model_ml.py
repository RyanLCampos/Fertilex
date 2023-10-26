import numpy as np
import pandas as pd
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import pickle
from sklearn.preprocessing import MinMaxScaler



def treinar_modelo(colunas_selecionadas, aplicar_smote):

    modelo_path = './Modelo/modelo_ml.sav'
    scaler_path = './Modelo/scaler.sav'
    if os.path.exists(modelo_path):
        os.remove(modelo_path)

    if os.path.exists(scaler_path):
        os.remove(scaler_path)

    # Obtém o diretório do script atual
    script_dir = os.path.dirname(__file__)

    # Constrói o caminho para 'dataset1.csv' dentro da estrutura do aplicativo Django
    dataset_path = os.path.join(script_dir, '', 'dataset1.csv')
    # Carregando dataset
    df = pd.read_csv(dataset_path)

    #colunas = 12 # Numero de colunas

    # Separando as features (X) e o rótulo de classe (y)
    #X = df.values[:, 0:colunas]  # Features (Exemplo: N,P,K,...)
    #Y = df.values[:, colunas]    # Rótulo de classe (Exemplo -> Output: 0,1 ou 2)

    # Excluindo colunas
    dataset = df.drop(columns=['B'])

    if colunas_selecionadas:
        X = dataset.loc[:, colunas_selecionadas]  # Features (Exemplo: N,P,K,...)
        Y = dataset["Output"]   # Rótulo de classe (Exemplo -> Output: 0,1 ou 2)
        print("Colunas selecionadas")
    else:
        colunas = 11 # Numero de colunas
        X = dataset.values[:, 0:colunas]  # Features (Exemplo: N,P,K,...)
        Y = dataset.values[:, colunas]    # Rótulo de classe (Exemplo -> Output: 0,1 ou 2)
        print("Colunas Padrão")

    if aplicar_smote:
        # Realizando o upsampling com SMOTE
        smote = SMOTE(sampling_strategy='auto', random_state=42)
        # Aplicar SMOTE apenas no dataset
        X_resampled, Y_resampled = smote.fit_resample(X, Y)
        print("Smote: ", X_resampled, Y_resampled)
    else:
        X_resampled = X
        Y_resampled = Y
        print("Não Smote: ", X_resampled, Y_resampled)

    # Separando para treino e teste (30% para teste)
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, Y_resampled, test_size=0.3, random_state=42)


    # ---- Aplicando Standar Scaler ----

    scaler = StandardScaler()
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("Dimensões de X_scaled:", X_train_scaled.shape)
    print("Dimensões de X_scaled:", X_test_scaled.shape)

    # ---- Utilizando modelo para treinamento ----

    clf = DecisionTreeClassifier(criterion = "entropy", class_weight='balanced',random_state = 100, max_depth = 7, min_samples_leaf = 7)
    clf.fit(X_train_scaled, y_train)

    modelo_path2 = os.path.join(os.path.dirname(__file__), 'modelo_ml.sav')
    with open(modelo_path2, 'wb') as modelo_arquivo:
        pickle.dump(clf, modelo_arquivo)
    
    scaler_path2 = os.path.join(os.path.dirname(__file__), 'scaler.sav')
    with open(scaler_path2, 'wb') as scaler_arquivo:
        pickle.dump(scaler, scaler_arquivo)
    
