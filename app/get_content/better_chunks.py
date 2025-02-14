import os
from openai import OpenAI
import json
from dotenv import load_dotenv
import tiktoken

load_dotenv(override=True)
my_api_key = os.getenv("OPENAI_API_KEY")

# Tokenizer für gpt-4 (oder gpt-3.5-turbo)
enc = tiktoken.encoding_for_model("gpt-4")

# Funktion zur Zählung der Token
def count_tokens(text):
    return len(enc.encode(text))

# Funktion zum Aufteilen des Textes in Teile
def split_text_into_chunks(text, max_tokens=6500):
    chunks = []
    current_chunk = ""
    current_tokens = 0
   
    for line in text:
        line_tokens = count_tokens(line)
        if current_tokens + line_tokens > max_tokens:
            chunks.append(current_chunk)
            current_chunk = line
            current_tokens = line_tokens
        else:
            current_chunk += " " + line
            current_tokens += line_tokens
   
    if current_chunk:
        chunks.append(current_chunk)
   
    return chunks

# Funktion zum Hinzufügen eines Elements zur JSON-Datei
def add_element_to_json(file_path, new_element):
    print("Füge Element hinzu:", new_element)
    # JSON-Datei einlesen
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Datei nicht gefunden, erstelle eine neue.")
        data = []

    # Überprüfen, ob die gelesenen Daten eine Liste sind
    if isinstance(data, list):
        data.append(new_element)
        print(f"Data: {data}")
    else:
        print("Die JSON-Datei enthält kein Array und das Element kann nicht hinzugefügt werden.")
        return
    
    # Geänderte Daten in die JSON-Datei zurückschreiben
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Element erfolgreich hinzugefügt.")

# Funktion zum Senden des Textes an das OpenAI API mit der Aufforderung, den Text zu verbessern
def send_text_to_openai_for_improvement(text):

    # Client-Instanz erstellen
    client = OpenAI(api_key=my_api_key)

    print("ein Durchgang")
    combined_text = " ".join(text)
    chunks = split_text_into_chunks(combined_text)
    responses = []
    for chunk in chunks:
        messages = [
            {"role": "user", "content": f"Bitte verbessere und überarbeite den folgenden Text, sodass er klarer und präziser wird, aber der Inhalt bleibt unverändert:{chunk}"}
        ]
       
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )

        response = completion.choices[0].message.content.strip()
        add_element_to_json("chunks.json", response)
        responses.append(response)  # Antwort zur Liste hinzufügen
    return responses