## 3. Dataset de intenções + Treinamento de modelo

INTENTS = {
    "greet": ["olá", "oi", "bom dia", "boa tarde", "boa noite"],
    "goodbye": ["tchau", "até logo", "encerrar", "sair"],
    "wikipedia_search": ["pesquise na wikipedia", "o que é", "quem é"],
    "open_youtube": ["abrir youtube", "youtube"],
    "find_pharmacy": ["farmácia", "drogaria", "próxima farmácia"],
    "open_website": ["abrir site", "ir para site"],
    "unknown": []
}

# Monta dataset de treino
TRAIN_SENTENCES, TRAIN_LABELS = [], []
for label, phrases in INTENTS.items():
    for p in phrases:
        TRAIN_SENTENCES.append(p)
        TRAIN_LABELS.append(label)

# Treina classificador simples
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=2000)
X_train = vectorizer.fit_transform(TRAIN_SENTENCES)
clf = LogisticRegression(max_iter=500)
clf.fit(X_train, TRAIN_LABELS)

def predict_intent(text: str):
    x = vectorizer.transform([text])
    probs = clf.predict_proba(x)[0]
    idx = probs.argmax()
    return clf.classes_[idx], float(probs[idx])
