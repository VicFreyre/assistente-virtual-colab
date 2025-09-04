

# 🤖 Assistente Virtual com PLN

Este projeto implementa um **sistema de assistência virtual** do zero, utilizando **Processamento de Linguagem Natural (PLN)** em Python.  O assistente reconhece comandos de voz, converte fala em texto, interpreta intenções e executa ações como abrir sites, pesquisar na Wikipédia ou localizar farmácias próximas.

<img width="738" height="246" alt="image" src="https://github.com/user-attachments/assets/67a4a7bc-48a7-4b18-8314-90366acf5499" />

[📂 Clique aqui para acessar o Colab](https://colab.research.google.com/drive/1UO3oX0Key_5DikNxDWK78HUl_pyRA7Hz#scrollTo=A1Pa0H65xhwd)

---

## 🚀 Funcionalidades
- **Speech to Text (STT)**: converte fala (áudio) em texto usando `SpeechRecognition`.
- **Text to Speech (TTS)**: gera respostas em áudio com `gTTS`.
- **Processamento de Linguagem Natural (PLN)**:
  - Classificação de intenções com `scikit-learn` e `TfidfVectorizer`.
  - Extração de entidades simples (Wikipedia, sites).
-  **Ações suportadas**:
  - Pesquisar na **Wikipédia**.
  - Abrir o **YouTube**.
  - Localizar farmácia próxima no **Google Maps**.
  - Acessar um site informado por voz.

---

## 📦 Tecnologias utilizadas
- Python
- SpeechRecognition
- gTTS
- Scikit-Learn
- NLTK
---

## 📂 Estrutura do Código

O notebook está dividido em células:

1. Instalação de pacotes
2. Imports e configuração
3. Dataset de intenções + Treinamento de modelo
4. Funções de Text-to-Speech
5. Funções de Speech-to-Text
6. Extração de entidades
7. Ações do assistente
8. Processamento de comandos
9. Loop principal de interação

---

## ▶️ Como Usar
1. Execute a célula de Loop
2. Sempre que o assistente solicitar um comando de voz, faça upload de um arquivo de áudio (.wav) usando o widget exibido
3. Receber resposta do assistente

---

##👩‍💻 Autora

[Victória Freyre](https://www.linkedin.com/in/vict%C3%B3ria-freyre-220b05291/)

