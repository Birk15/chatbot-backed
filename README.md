# KI-basierter Chatbot - Backend

Dieses Backend ermöglicht die Integration eines intelligenten Chatbots auf **beliebigen Webseiten**.
Der Chatbot beantwortet Nutzerfragen **ausschließlich auf Basis der auf der Webseite hinterlegten Inhalte**, ohne auf externe Datenquellen zurückzugreifen.

Entwickelt mit **Flask** und integriert mit **OpenAI**, bietet dieses System:
- **Kontextbezogene Antworten** durch Vektorisierung und Ähnlichkeitssuche.
- **Anpassbare Wissensbasis**, die automatisch aus den Inhalten der Webseite generiert wird.
- **Einfache Integration** als REST-API für flexible Frontend-Anbindungen.

Das Ziel dieses Projekts ist es, Webseitenbesuchern **relevante und präzise Informationen** zu bieten, indem nur vorhandene Daten verwendet werden.


## Verwendete Technologien
- Python 3.x
- Flask (Backend-Framework)
- OpenAI API (Chat-Generierung)
- FAISS (Vektorsuche und Ähnlichkeitsberechnung)
- Sentence Transformers (Vektorisierung)
- Requests (HTTP-Anfragen an APIs)  
- BeautifulSoup (HTML-Parsing für Web-Inhalte)  


## Voraussetzungen
- Python 3.x
- OpenAI API Key (für die Nutzung von GPT-3 oder GPT-4)


## Installation und Setup

1. Repository klonen:
    ```bash
    git clone <URL_DEINES_REPOS>
    cd chatbot-backend
    ```

2. Virtuelle Umgebung erstellen und aktivieren:
    ```bash
    python -m venv venv
    . venv/bin/activate  # Für Linux/Mac
    venv\Scripts\activate  # Für Windows
    ```

3. Abhängigkeiten installieren:
    ```bash
    pip install -r requirements.txt
    ```

4. Konfiguration anpassen:
    Erstelle eine `.env`-Datei und füge deinen OpenAI API Key hinzu:
    ```env
    OPENAI_API_KEY=dein_api_key
    ```

5. Anwendung starten (je nach Python-Version mit `py`, `python` oder `python3`):
    ```bash
    py main.py
    ```
    


## API-Endpunkte

### POST /chat
- **Beschreibung:** Sendet eine Nutzeranfrage und erhält eine KI-generierte Antwort.
- **Anfrage:** 
    ```json
    {
      "text": "Wie ist das Wetter heute?",
      "url": "https://www.example.com"
    }
    ```
- **Antwort:**
    ```json
    {
      "reply": "Das Wetter heute ist sonnig mit 25°C."
    }
    ```

### GET /test
- **Beschreibung:** Überprüft den Status des Backends.
- **Antwort:**
    ```json
    {
      "message": "Success!"
    }
    ```


## Mitwirkende
- [Birk Dinkelacker](https://github.com/Birk15)

