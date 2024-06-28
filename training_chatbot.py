import streamlit as st
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model # type: ignore

# Cargar los datos necesarios (intents, words, classes, model)
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents_spanish.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

# Funciones para el procesamiento del texto
def clean_up_sentence(sentence):
    """Tokeniza y lematiza una oración."""
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words, show_details=True):
    """Convierte una oración en una bolsa de palabras."""
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
                if show_details:
                    print(f"Found in bag: {word}")
    return np.array(bag)

# Función para predecir la intención del usuario
def predict_class(sentence):
    """Predice la intención de la oración del usuario."""
    bow = bag_of_words(sentence, words, show_details=False)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Función para obtener la respuesta del chatbot
def get_response(intents_list):
    """Genera una respuesta basada en la intención predecida."""
    tag = intents_list[0]['intent']
    list_of_intents = intents['intents']
    for intent in list_of_intents:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            break
    else:
        response = "No entendí tu pregunta, ¿podrías ser más específico?"
    return response

# Configuración de Streamlit para la interfaz de usuario
st.title("Chatbot")
st.write("¡Hola! Soy un chatbot. ¿En qué puedo ayudarte?")

# Entrada de texto del usuario
user_input = st.text_input("Tú: ", "")

if user_input:
    # Predice la intención de la entrada del usuario
    predicted_intents = predict_class(user_input)
    # Genera la respuesta del chatbot
    response = get_response(predicted_intents)
    # Muestra la respuesta del chatbot
    st.text_area("Chatbot: ", value=response, height=200, max_chars=None, key=None)
