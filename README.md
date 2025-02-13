# KI-basierter Chatbot - Backend

Dieses Backend ermöglicht die Integration eines intelligenten Chatbots auf **beliebigen Webseiten**.
Der Chatbot beantwortet Nutzerfragen **ausschließlich auf Basis der auf der Webseite hinterlegten Inhalte**, ohne auf externe Datenquellen zurückzugreifen.

Entwickelt mit **Flask** und integriert mit **OpenAI**, bietet dieses System:
- **Kontextbezogene Antworten** durch Vektorisierung und Ähnlichkeitssuche.
- **Anpassbare Wissensbasis**, die automatisch aus den Inhalten der Webseite generiert wird.
- **Einfache Integration** als REST-API für flexible Frontend-Anbindungen.
- 
Das Ziel dieses Projekts ist es, Webseitenbesuchern **relevante und präzise Informationen** zu bieten, indem nur vorhandene Daten verwendet werden.


## Verwendete Technologien
- Python 3.x
- Flask (Backend-Framework)
- OpenAI API (Chat-Generierung)
- FAISS (Vektorsuche und Ähnlichkeitsberechnung)
- Sentence Transformers (Vektorisierung)
- Requests (HTTP-Anfragen an APIs)  
- BeautifulSoup (HTML-Parsing für Web-Inhalte)  

