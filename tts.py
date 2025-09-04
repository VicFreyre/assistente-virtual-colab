## 4. Funções de Text-to-Speech

def falar(texto, filename="resposta.mp3"):
    print("Assistente:", texto)
    tts = gTTS(texto, lang="pt")
    tts.save(filename)
    display(Audio(filename, autoplay=True))
