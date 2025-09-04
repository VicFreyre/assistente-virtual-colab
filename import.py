## 2. Imports e configuração

import os, re, time, random
import wikipedia, webbrowser, speech_recognition as sr

# PLN / ML
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# TTS para Colab
from gtts import gTTS
from IPython.display import Audio, display

# NLTK (tokenização, se necessário)
import nltk
nltk.download("punkt", quiet=True)

# Escolha o modo: "colab" (upload de áudio) ou "local" (microfone)
MODE = "colab"
