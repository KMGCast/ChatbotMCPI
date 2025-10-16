from django.shortcuts import render
from django.http import JsonResponse
import joblib
import os
from .respuestas import RESPUESTAS_AUTOMATICAS

#Rutas a modelos: 
MODELO_PATH= os.path.join('modelo','tutorMCPI_modelo.joblib')
VECTORIZADOR_PATH=os.path.join('modelo','tutorMCPI_vectorizador.joblib')

#Cargar
try:
    modelo=joblib.load(MODELO_PATH)
    vectorizador=joblib.load(VECTORIZADOR_PATH)
    MODELO_CARGADO= True
except Exception as e:
    modelo=None
    vectorizador=None
    MODELO_CARGADO= False

#Función

def chatbot_response(request):
    if request.method == "POST":
        if not MODELO_CARGADO:
            return JsonResponse({'respuesta': RESPUESTAS_AUTOMATICAS.get('default', 'Error: Modelo no cargado') + "**(Modelo no cargado)**"})
        
        pregunta = request.POST.get("pregunta", '').lower().strip()
        
        try:
            pregunta_vectorizada = vectorizador.transform([pregunta])
            etiqueta_predicha = modelo.predict(pregunta_vectorizada)[0]  # predicción devuelve lista, toma el primero
            
            respuesta = RESPUESTAS_AUTOMATICAS.get(etiqueta_predicha, RESPUESTAS_AUTOMATICAS.get('default', 'Sin respuesta disponible'))
            
            return JsonResponse({'respuesta': respuesta, 'etiqueta': etiqueta_predicha})
        except Exception as e:
            return JsonResponse({'respuesta': RESPUESTAS_AUTOMATICAS.get('default', 'Error') + f" (Error: {e})"})
    
    # Para otros métodos, renderizamos la plantilla (GET por ejemplo)
    return render(request, 'chatbot_app/chatbot.html')
