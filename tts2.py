## 5. Funções de Speech-to-Text

from google.colab import files

def carregar_audio():
    print("📂 Faça upload de um arquivo de áudio (.wav)")
    uploaded = files.upload()
    for filename in uploaded.keys():
        return filename
    return None

def ouvir_arquivo(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
        print("👉 Você disse:", texto)
        return texto.lower()
    except:
        return ""
