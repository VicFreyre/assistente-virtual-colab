## 7. Ações do assistente

def action_wikipedia(query):
    if not query:
        falar("Sobre o que você deseja saber na Wikipédia?")
        return
    try:
        wikipedia.set_lang("pt")
        resumo = wikipedia.summary(query, sentences=2)
        falar(resumo)
    except:
        falar("Não encontrei informações na Wikipédia.")

def action_open_youtube():
    falar("Abrindo YouTube...")
    webbrowser.open("https://www.youtube.com")

def action_find_pharmacy():
    falar("Buscando farmácia mais próxima...")
    webbrowser.open("https://www.google.com/maps/search/farmácia+próxima/")

def action_open_website(text):
    url = extract_website(text)
    if url:
        falar(f"Abrindo {url}")
        webbrowser.open(url)
    else:
        falar("Não consegui identificar o site para abrir.")
