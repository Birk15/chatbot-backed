import requests

def ask_ollama(user_message, context):
    prompt = f"Hier sind relevante Informationen:\n\n{context}\n\nAntworte nur mit diesen Informationen. Falls nichts Passendes dabei ist, sag 'Ich weiß es nicht.'\n\nFrage: {user_message}"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "num_predict": 10,  # Versuche erneut, die Tokens zu begrenzen
                "temperature": 0.3, 
                "top_k": 10,
                "top_p": 0.5,
                "mirostat": 2,
                "mirostat_tau": 2.0,
                "stop": ["\n", ".", "?"],  # Zusätzliche Stop-Sequenzen
            }
        )

        # Debugging: API-Rohantwort ausgeben
        response_data = response.json()

        # Überprüfung, bevor "response" aufgerufen wird
        if "response" not in response_data:
            print("Ollama hat keine gültige Antwort geliefert!")
            return "Ich konnte leider keine Antwort generieren."

        return response_data["response"]

    except Exception as e:
        print(f"API-Fehler: {e}")
        return "Ein Fehler ist aufgetreten. Bitte versuche es später erneut."



