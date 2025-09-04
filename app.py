import os
import re
import sys
import time
import wikipedia
import webbrowser
import threading

# NLP & ML
import random
import string
from typing import Tuple, Optional, List

# scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Speech and TTS
import speech_recognition as sr

# We'll try to import both TTS options; if missing, we'll fallback gracefully
try:
    import pyttsx3  # local TTS
except Exception:
    pyttsx3 = None

try:
    from gtts import gTTS  # Colab / web TTS
    from IPython.display import Audio, display  # only available in notebook
except Exception:
    gTTS = None
    Audio = None
    display = None

# Optional: download NLTK punkt for tokenization if not present
try:
    import nltk
    nltk.data.find("tokenizers/punkt")
except Exception:
    try:
        import nltk
        nltk.download("punkt", quiet=True)
    except Exception:
        pass

# -----------------------
# Configurações / Modo
# -----------------------
# Escolha "local" ou "colab".
# Se estiver em Colab, use "colab" (upload de áudios). Local, use "local".
MODE = "local"  # alterar para "colab" se for usar no Google Colab

# -----------------------
# Base de intenções (dataset simples para treinar o classificador)
# -----------------------
INTENTS = {
    "greet": [
        "olá", "oi", "bom dia", "boa tarde", "boa noite", "e aí", "salve", "hey assistente"
    ],
    "goodbye": [
        "tchau", "até logo", "adeus", "encerrar", "sair", "até mais"
    ],
    "wikipedia_search": [
        "pesquise na wikipedia", "procure na wikipedia", "wikipedia sobre", "o que é", "quem é",
        "me conte sobre", "pesquisar", "busca sobre"
    ],
    "open_youtube": [
        "abrir youtube", "youtube", "abre o youtube", "procure no youtube", "tocar no youtube"
    ],
    "find_pharmacy": [
        "farmácia", "drogaria", "encontrar farmácia", "onde tem farmácia", "próxima farmácia"
    ],
    "open_website": [
        "abrir site", "abrir o site", "abrir", "ir para", "abrir o"
    ],
    "unknown": [
        # exemplos vazios — classe para fallback
    ]
}

# Add some synthetic patterns combining words
TRAIN_SENTENCES = []
TRAIN_LABELS = []
for label, phrases in INTENTS.items():
    for p in phrases:
        TRAIN_SENTENCES.append(p)
        TRAIN_LABELS.append(label)

# Add some extra variations for training (small augmentation)
extra_examples = [
    ("procure por {} no wikipedia", "wikipedia_search"),
    ("quero saber sobre {}", "wikipedia_search"),
    ("me mostra {} no youtube", "open_youtube"),
    ("abre o site {}", "open_website"),
    ("onde fica a farmácia mais próxima", "find_pharmacy"),
]
# We'll add placeholder examples using common topics
placeholders = ["vacinas", "python", "estados unidos", "paracetamol"]

for tmpl, label in extra_examples:
    for ph in placeholders:
        TRAIN_SENTENCES.append(tmpl.format(ph))
        TRAIN_LABELS.append(label)

# -----------------------
# Treinamento do classificador simples
# -----------------------
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=2000)
X_train = vectorizer.fit_transform(TRAIN_SENTENCES)
clf = LogisticRegression(max_iter=500)
clf.fit(X_train, TRAIN_LABELS)

def predict_intent(text: str) -> Tuple[str, float]:
    """
    Retorna (intent, confidence)
    """
    if not text or text.strip() == "":
        return "unknown", 0.0
    x = vectorizer.transform([text])
    probs = clf.predict_proba(x)[0]
    idx = probs.argmax()
    intent = clf.classes_[idx]
    return intent, float(probs[idx])

# -----------------------
# Utilitários de extração de entidade (very simple)
# -----------------------
def extract_wikipedia_query(text: str) -> str:
    """
    Extrai a consulta principal para pesquisa na Wikipedia.
    Estratégia simples:
    - Remover palavras-chave como 'pesquise', 'wikipedia', 'o que é', etc.
    - Pegar a parte restante do texto.
    """
    text = text.lower()
    # Remove trigger words
    triggers = ["pesquise", "pesquisar", "procure", "procure por", "wikipedia", "na wikipedia", "o que é", "quem é", "me conte sobre", "me mostre"]
    for t in triggers:
        text = text.replace(t, "")
    # Remove filler words
    text = re.sub(r"\b(na|no|sobre|sobre o|sobre a|por favor|por favor,?)\b", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_website(text: str) -> Optional[str]:
    """
    Tenta extrair um site/termo para abrir.
    Ex: 'abrir site da globo' -> 'globo'
    Se detecta um URL, retorna ele.
    """
    # busca url explícita
    m = re.search(r"(https?://[^\s]+)", text)
    if m:
        return m.group(1)
    # pega termo após 'abrir' ou 'ir para'
    m2 = re.search(r"(abrir|ir para|abre|abrir o site|abrir site)\s+(.*)", text)
    if m2:
        term = m2.group(2)
        term = term.strip()
        # se for palavra única, añade https://www.{term}.com
        if " " not in term and "." not in term:
            return f"https://www.{term}.com"
        if "." in term:
            if not term.startswith("http"):
                return "http://" + term
            return term
        return "https://www.google.com/search?q=" + term.replace(" ", "+")
    return None

# -----------------------
# Funções de TTS
# -----------------------
def tts_local(text: str):
    """TTS offline usando pyttsx3"""
    if pyttsx3 is None:
        print("[TTS] pyttsx3 não encontrado.")
        return
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()

def tts_colab_play(text: str, filename: str = "resposta.mp3"):
    """TTS usando gTTS e reproduz (no notebook)"""
    if gTTS is None:
        print("[TTS] gTTS não disponível.")
        return
    tts = gTTS(text, lang="pt")
    tts.save(filename)
    if Audio and display:
        display(Audio(filename, autoplay=True))
    else:
        print(f"[TTS] Áudio salvo em {filename}")

def falar(text: str):
    """Wrapper para TTS dependendo do modo."""
    print("Assistente:", text)
    if MODE == "local":
        tts_local(text)
    else:
        # Colab / fallback
        tts_colab_play(text)

# -----------------------
# STT: ouvir do microfone (local) ou processar arquivo (colab)
# -----------------------
def ouvir_microfone_local(timeout: int = 5, phrase_time_limit: Optional[int]=7) -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando ruído ambiente...")
        r.adjust_for_ambient_noise(source, duration=1.0)
        print("Diga algo...")
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("Tempo esgotado, nada foi capturado.")
            return ""
    try:
        texto = r.recognize_google(audio, language="pt-BR")
        print("Você disse:", texto)
        return texto.lower()
    except sr.UnknownValueError:
        print("Não entendi o áudio.")
        return ""
    except sr.RequestError as e:
        print("Erro ao conectar ao serviço de reconhecimento:", e)
        return ""

def ouvir_arquivo_colab(path: str) -> str:
    r = sr.Recognizer()
    try:
        with sr.AudioFile(path) as source:
            audio = r.record(source)
        texto = r.recognize_google(audio, language="pt-BR")
        print("Transcrição:", texto)
        return texto.lower()
    except Exception as e:
        print("Erro ao processar arquivo:", e)
        return ""

# -----------------------
# Ações (intenções mapeadas)
# -----------------------
def action_wikipedia(query: str):
    if not query:
        falar("Sobre o que você quer saber na Wikipédia?")
        return
    falar(f"Buscando {query} na Wikipédia...")
    try:
        wikipedia.set_lang("pt")
        resumo = wikipedia.summary(query, sentences=2, auto_suggest=True)
        print("Wikipedia resumo:", resumo)
        falar(resumo)
    except Exception as e:
        print("Erro Wikipédia:", e)
        falar("Desculpe, não encontrei resultados na Wikipédia.")

def action_open_youtube(query: Optional[str]=None):
    if query:
        # busca no YouTube
        q = query.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={q}"
    else:
        url = "https://www.youtube.com"
    falar("Abrindo YouTube...")
    webbrowser.open(url)

def action_find_pharmacy():
    falar("Mostrando farmácias próximas no Google Maps...")
    webbrowser.open("https://www.google.com/maps/search/farmácia+próxima/")

def action_open_website(term: str):
    url = extract_website(term)
    if url:
        falar(f"Abrindo {url}")
        webbrowser.open(url)
    else:
        falar("Não consegui identificar o site para abrir.")

def action_unknown():
    falar("Desculpe, não entendi. Poderia repetir de outra forma?")

# -----------------------
# Pipeline de processamento do comando
# -----------------------
def process_command_text(text: str):
    intent, conf = predict_intent(text)
    print(f"[PLN] Intent prevista: {intent} (conf={conf:.2f})")

    # Regra simples para detectar comandos explícitos
    if "wikipedia" in text or intent == "wikipedia_search" or any(kw in text for kw in ["o que é", "quem é", "me conte sobre", "pesquise"]):
        query = extract_wikipedia_query(text)
        # se query vazio, tentamos remover o trigger e usar o resto
        if not query:
            # tenta extrair texto entre "sobre" e fim
            m = re.search(r"sobre (.*)", text)
            query = m.group(1) if m else ""
        action_wikipedia(query)
        return

    if "youtube" in text or intent == "open_youtube" or "tocar" in text and "youtube" in text:
        # extrai termo de busca
        m = re.search(r"youtube (sobre|de|de )?(.*)", text)
        query = None
        if m:
            query = m.group(2).strip()
        action_open_youtube(query)
        return

    if "farmácia" in text or intent == "find_pharmacy" or any(kw in text for kw in ["drogaria", "onde tem farmácia", "farmacia"]):
        action_find_pharmacy()
        return

    if "abrir" in text or intent == "open_website":
        action_open_website(text)
        return

    if intent == "greet":
        falar(random.choice(["Olá! Em que posso ajudar?", "Oi! Como posso te ajudar hoje?"]))
        return

    if intent == "goodbye":
        falar(random.choice(["Até logo!", "Tchau!"]))
        # indicate termination if used from main loop
        return "terminate"

    # fallback
    action_unknown()
    return

# -----------------------
# Loop principal: local ou colab
# -----------------------
def run_assistant_local():
    falar("Olá! Sou sua assistente virtual. Diga 'sair' para encerrar.")
    while True:
        texto = ouvir_microfone_local()
        if not texto:
            # se silencioso, tenta novamente
            continue
        if any(word in texto for word in ["sair", "encerrar", "tchau", "até mais"]):
            falar("Encerrando. Até logo!")
            break
        result = process_command_text(texto)
        if result == "terminate":
            break
        # pequeno intervalo para não ficar em loop instantâneo
        time.sleep(0.5)

def run_assistant_colab():
    """
    Em Colab, pedimos upload de arquivo de áudio por iteração.
    Simples: o usuário faz upload e o assistente processa.
    """
    from google.colab import files
    falar("Olá! Envie um arquivo de áudio (.wav) com seu comando. Envie 'sair' como comando de voz para encerrar.")
    while True:
        print("Faça upload do arquivo de áudio (.wav/.mp3):")
        uploaded = files.upload()
        if not uploaded:
            print("Nenhum arquivo enviado.")
            continue
        # pega primeiro arquivo
        filename = list(uploaded.keys())[0]
        print("Arquivo recebido:", filename)
        texto = ouvir_arquivo_colab(filename)
        if not texto:
            continue
        if any(word in texto for word in ["sair", "encerrar", "tchau", "até mais"]):
            falar("Encerrando. Até logo!")
            break
        result = process_command_text(texto)
        if result == "terminate":
            break
        time.sleep(0.5)

# -----------------------
# Execução
# -----------------------
if __name__ == "__main__":
    # detect environment: if running inside IPython/Colab and MODE not set to local, keep colab.
    in_ipython = False
    try:
        get_ipython  # type: ignore
        in_ipython = True
    except Exception:
        in_ipython = False

    if MODE == "colab" or (MODE != "local" and in_ipython):
        print("Executando no modo COLAB/upload.")
        run_assistant_colab()
    else:
        print("Executando no modo LOCAL (microfone).")
        run_assistant_local()
