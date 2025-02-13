from sentence_transformers import SentenceTransformer  # KI-Modell zur Textvektorisierung
import os
import json
import faiss
from app.config import Config
from app.get_content.vektordb import create_vektor_db

def get_context(query, web_url, top_k=10):  # Hole mehr Ergebnisse, um später zu filtern
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    # Aktuelles Verzeichnis des Skripts holen
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Datei-Pfade für den FAISS-Index und Chunks erstellen
    index_file = os.path.join(BASE_DIR, "get_content", Config.INDEX_FILE)
    chunks_file = os.path.join(BASE_DIR, "get_content", Config.CHUNKS_FILE)

    # Prüfen, ob Index existiert
    if os.path.exists(index_file) and os.path.exists(chunks_file):
        print("Lade bestehenden FAISS-Index und Chunks...")
        index = faiss.read_index(index_file)

        # Chunks aus Datei laden
        with open(chunks_file, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    else:
        index, chunks = create_vektor_db(model, Config.INDEX_FILE, Config.CHUNKS_FILE, web_url)
    
    # Frage als Embedding berechnen
    frage_embedding = model.encode(query, convert_to_numpy=True, normalize_embeddings=True).reshape(1, -1)

    similarities, idx = index.search(frage_embedding, top_k)

    for j, i in enumerate(idx[0]):
        print(f"Chunk-Index: {i} | Rang: {j} | Cosine Similarity: {similarities[0][j]:.4f}")

    # Nur Ergebnisse mit Score > 0.3 behalten
    filtered_results = [(chunks[i], similarities[0][j]) for j, i in enumerate(idx[0]) if similarities[0][j] >= 0.3]

    # Duplikate anhand des Textinhalts filtern
    unique_chunks = []
    seen_chunks = set()

    for chunk, sim in filtered_results:
        # Duplikate anhand des Textes vermeiden
        if chunk not in seen_chunks:
            seen_chunks.add(chunk)
            unique_chunks.append((chunk, sim))
    
    # Nach Similarity sortieren und die besten auswählen
    unique_chunks.sort(key=lambda x: x[1], reverse=True)
    results = [x[0] for x in unique_chunks[:5]]  # Nimm die besten 5

    # Falls zu wenig relevante Ergebnisse, trotzdem 3 zurückgeben
    if len(results) < 3:
        results = [x[0] for x in unique_chunks]

    return results
