from openai import OpenAI
from ..config import Config

def ask_openai(user_message, context):
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    # Die Eingabe wird aus dem Kontext und der Benutzer-Nachricht zusammengesetzt
    prompt = f"Context: {context}\nUser: {user_message}\nAI:"
    
    try:
        messages = [
            {"role": "system", "content": "Du bist ein hilfreicher Assistent, der auf Grundlage des gegebenen Kontexts antwortet."},
            {"role": "user", "content": prompt}
        ]
        
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
            max_tokens=150,
            temperature=0.5
        )

        # Antwort zusammenbauen
        response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content

        return response
    
    except Exception as e:
        print(f"Fehler bei der Anfrage an OpenAI: {e}")
        return "Es gab ein Problem bei der Kommunikation mit OpenAI."
