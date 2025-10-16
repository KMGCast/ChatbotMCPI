import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
import os
import joblib

#Cargando datos: 
data_path=os.path.join('data','preguntas.csv')
dataset=pd.read_csv(data_path)
print (f"Data ser cargado con {len(dataset)} preguntas de ejemplo ")

#Vectorizando los textos con TfidVext
vectorizador=TfidfVectorizer(ngram_range=(1,2),max_features=1000)
X=vectorizador.fit_transform(dataset['pregunta'])
y=dataset['etiqueta']

#Separar datos: 
X_train,X_test,y_train,y_test = train_test_split(X,y, test_size=0.2,stratify=y, random_state=42)

#Hiperparámetros para el mejor modelo
parametros = {
    'C': [0.1, 1, 10],
    'solver': ['liblinear', 'lbfgs']
}

grid = GridSearchCV(LogisticRegression(max_iter=1000, random_state=42),
                    parametros, cv=5, scoring='accuracy')

grid.fit(X_train, y_train)

mejor_modelo = grid.best_estimator_

#Modelo + entrenamiento
y_pred=mejor_modelo.predict(X_test)
#Guardar
joblib.dump(mejor_modelo,'modelo/tutorMCPI_modelo.joblib')
joblib.dump(vectorizador,'modelo/tutorMCPI_vectorizador.joblib')