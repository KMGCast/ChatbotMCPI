import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
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

#Modelo + entrenamiento
modelo=LogisticRegression(max_iter=1000, random_state=42)
modelo.fit(X,y)

#Guardar
joblib.dump(modelo,'modelo/tutorMCPI_modelo.joblib')
joblib.dump(vectorizador,'modelo/tutorMCPI_vectorizador.joblib')