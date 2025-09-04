## 6. Extração de entidades

def extract_wikipedia_query(text: str):
    triggers = ["pesquise", "wikipedia", "o que é", "quem é", "me conte sobre"]
    for t in triggers:
        text = text.replace(t, "")
    return text.strip()

def extract_website(text: str):
    if "http" in text:
        return text.split()[-1]
    m = re.search(r"site (.+)", text)
    if m:
        return "https://www." + m.group(1).replace(" ", "") + ".com"
    return None
