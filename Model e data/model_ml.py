import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import pickle

# Carregando dataset
df = pd.read_csv('dataset1.csv')

#colunas = 12 # Numero de colunas

# Separando as features (X) e o rótulo de classe (y)
#X = df.values[:, 0:colunas]  # Features (Exemplo: N,P,K,...)
#Y = df.values[:, colunas]    # Rótulo de classe (Exemplo -> Output: 0,1 ou 2)

# Excluindo colunas
dataset = df.drop(columns=['B'])

colunas = 11 # Numero de colunas
X = dataset.values[:, 0:colunas]  # Features (Exemplo: N,P,K,...)
Y = dataset.values[:, colunas]    # Rótulo de classe (Exemplo -> Output: 0,1 ou 2)


# Realizando o upsampling com SMOTE
smote = SMOTE(sampling_strategy='auto', random_state=42)

# Aplicar SMOTE apenas no dataset
X_resampled, Y_resampled = smote.fit_resample(X, Y)


# Separando para treino e teste (30% para teste)
X_train, X_test, y_train, y_test = train_test_split(X_resampled, Y_resampled, test_size=0.3, random_state=42)

# ---- Aplicando Standar Scaler ----
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---- Utilizando modelo para treinamento ----

# Função para performar o treinamento com Entropy
clf = DecisionTreeClassifier(criterion = "entropy", class_weight='balanced',random_state = 100, max_depth = 7, min_samples_leaf = 7)
clf.fit(X_train_scaled, y_train)

pickle.dump(clf, open("modelo_ml.sav", "wb"))
pickle.dump(scaler, open("scaler.sav", "wb"))