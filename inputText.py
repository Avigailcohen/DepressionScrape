import warnings
warnings.filterwarnings("ignore")
import ftfy
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import re

from math import exp
from numpy import sign

from sklearn.metrics import  classification_report, confusion_matrix, accuracy_score
from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from nltk import PorterStemmer

from keras.models import Model, Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Conv1D, Dense, Input, LSTM, Embedding, Dropout, Activation, MaxPooling1D
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import plot_model


from keras.models import load_model
import pickle

model_pkl_file="model.pkl"
with open(model_pkl_file,'rb') as file:
    model = pickle.load(file)
# Load tokenizer and define MAX_SEQUENCE_LENGTH accordingly
# Load tokenizer and define MAX_SEQUENCE_LENGTH accordingly
tokenizer_pkl_file = "tokenizer.pkl"
with open(tokenizer_pkl_file, 'rb') as file:
    tokenizer = pickle.load(file)

MAX_SEQUENCE_LENGTH = 140  # Adjust this based on your model's training configuration#clean the input

def preprocess_input_text(text):
    # Clean the text
    text = ftfy.fix_text(text)  # Fix text encoding issues
   # text = expandContractions(text)  # Expand contractions using the predefined dictionary
    text = re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text)  # Remove unwanted characters
    text = text.lower()  # Convert to lowercase
    tokens = nltk.word_tokenize(text)  # Tokenize
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    
    # Stemming (optional)
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in tokens]
    
    # Convert to sequence
    #sequence = tokenizer.texts_to_sequences([stemmed])
    # Convert to sequence using the loaded tokenizer
    sequence = tokenizer.texts_to_sequences([stemmed])
    padded_sequence = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH)
    
    return padded_sequence


def predict_depression(text, threshold=0.25):  # Adjust the threshold here
    preprocessed_text = preprocess_input_text(text)
    prediction_proba = model.predict(preprocessed_text)
    
    prediction_class = (prediction_proba >= threshold).astype(int)
    return "Depressive" if prediction_class[0][0] == 1 else "Non-depressive"

#if __name__ == "__main__":
 #   predict_depression("help")    
    #print(f"Prediction: {prediction}")