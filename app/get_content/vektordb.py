import faiss  # FAISS (Facebook AI Similarity Search) für schnelle Vektor-Suche
import numpy as np  # Für effiziente numerische Berechnungen
from .crawl import text_result  # Funktion, die eine Webseite scrapt
import json # Chunks in einem JSON File speichern
import os
from app.get_content.better_chunks import send_text_to_openai_for_improvement

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

    # Chunks erstellen
    chunks = []

    for item in scraped_data:        
        # Text speichern für die Chunks-Datei
        combined_text = f"{item['Thema']}: {item['Text']}"
        chunks.append(combined_text)

    final_chunks = send_text_to_openai_for_improvement(chunks)
    print(f"Final Chunks: {final_chunks}")


    # Vektoren erstellen
    embeddings = []

    for item in final_chunks:
        vec = model.encode(item)
        embeddings.append(vec)
    
    embeddings = np.array(embeddings)
    print(f"Embeddings Shape: {embeddings.shape}")

    # FAISS Index erstellen
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    # FAISS-Index speichern
    faiss.write_index(index, index_file)

    # Chunks speichern
    with open(chunks_file, "w", encoding="utf-8") as f:
        json.dump(final_chunks, f, ensure_ascii=False, indent=4)

    return index, final_chunks

