import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents_spanish.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

def save_interaction(user_input, predicted_intent, confidence, actual_intent=None):
    data = {
        "user_input": user_input,
        "predicted_intent": predicted_intent,
        "confidence": confidence,
        "actual_intent": actual_intent
    }
    with open('interactions_log.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
                if show_details:
                    print(f"Found in bag: {word}")
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list):
    tag = intents_list[0]['intent']
    list_of_intents = intents['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            response = random.choice(i['responses'])
            break
    else:
        response = "No entendí tu pregunta, ¿podrías ser más específico?"
    return response
# Función para guardar interacciones
def save_interaction(prompt, intent, probability, actual_intent=None):
    # Implementa la lógica para guardar la interacción
    pass

# Otras funciones y lógica del chatbot...
