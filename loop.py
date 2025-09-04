##  9. Loop principal de interação

def assistente_virtual():
    falar("Olá! Sou sua assistente virtual no Colab. Envie um áudio com seu comando.")
    while True:
        audio_path = carregar_audio()
        if audio_path:
            comando = ouvir_arquivo(audio_path)
            if comando:
                if "sair" in comando or "encerrar" in comando:
                    falar("Encerrando. Até logo!")
                    break
                result = process_command_text(comando)
                if result == "terminate":
                    break

assistente_virtual()
