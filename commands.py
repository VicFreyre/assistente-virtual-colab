## 8. Processamento de comandos

def process_command_text(text: str):
    intent, conf = predict_intent(text)
    print(f"[PLN] Intent prevista: {intent} (conf={conf:.2f})")

    if intent == "wikipedia_search":
        query = extract_wikipedia_query(text)
        action_wikipedia(query)

    elif intent == "open_youtube":
        action_open_youtube()

    elif intent == "find_pharmacy":
        action_find_pharmacy()

    elif intent == "open_website":
        action_open_website(text)

    elif intent == "greet":
        falar("Olá! Em que posso ajudar?")

    elif intent == "goodbye":
        falar("Até logo!")
        return "terminate"

    else:
        falar("Desculpe, não entendi.")
