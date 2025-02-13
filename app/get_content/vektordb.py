import faiss  # FAISS (Facebook AI Similarity Search) für schnelle Vektor-Suche
import numpy as np  # Für effiziente numerische Berechnungen
from .crawl import text_result  # Funktion, die eine Webseite scrapt
import json # Chunks in einem JSON File speichern
import os

def create_vektor_db(model, INDEX_FILE, CHUNKS_FILE, web_url):

    # Aktuelles Verzeichnis des Skripts holen
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Datei-Pfade für den FAISS-Index und Chunks erstellen
    index_file = os.path.join(BASE_DIR, INDEX_FILE)
    chunks_file = os.path.join(BASE_DIR, CHUNKS_FILE)

    print("Kein Index gefunden, scrapen und erstellen...")

    scraped_data = text_result(web_url)  # Webseite scrapen

    print(f"Data {scraped_data}")

     # Überprüfen, ob Daten vorhanden sind
    if not scraped_data:
        print("Fehler: Keine Daten gefunden.")
        return None, None

    # Vektoren erstellen und Gewichtung anwenden
    embeddings = []
    chunks = []

    for item in scraped_data:
        # Überschrift und Text getrennt vektorisieren
        headline_vec = model.encode(item["Thema"])  # Nur die Überschrift
        content_vec = model.encode(item["Text"])  # Nur der Inhalt
        
        # Gewichtung nur auf die Überschrift anwenden
        headline_vec *= item["Gewichtung"]
        
        # Überschrift und Inhalt kombinieren
        combined_vec = headline_vec + content_vec
        embeddings.append(combined_vec)
        
        # Text speichern für die Chunks-Datei
        combined_text = f"{item['Thema']}: {item['Text']}"
        chunks.append(combined_text)

    embeddings = np.array(embeddings)

    # FAISS Index erstellen
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    # FAISS-Index speichern
    faiss.write_index(index, index_file)

    print(f"Chunks: {chunks}")

    # Chunks speichern
    with open(chunks_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)

    return index, chunks

