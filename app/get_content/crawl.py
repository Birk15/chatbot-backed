import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from .cleantext import clean_text

visited_links = set()  # Set für besuchte Links
result = []  # Gespeicherte Inhalte

# Funktion zur URL-Normalisierung
def normalize_url(url):
    # URL in Bestandteile zerlegen
    parsed_url = urlparse(url)
    
    # Anker entfernen und Trailing Slash bereinigen
    normalized_url = parsed_url._replace(fragment="")._replace(path=parsed_url.path.rstrip('/'))
    
    # URL wieder zusammenbauen
    return urlunparse(normalized_url)

# Hauptfunktion für das Crawling
def crawl(url):
    print(f"Crawling: {url}")
    
    base_url = url
    
    # Überprüfen, ob URL schon besucht wurde
    if url in visited_links:
        return
    visited_links.add(url)
    
    # Abrufen der Seite
    try:
        response = requests.get(url)
        response.raise_for_status()  # Überprüfen auf HTTP-Fehler
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen von {url}: {e}")
        return
    
    # Versuchen, das HTML zu parsen
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Fehler beim Parsen von {url}: {e}")
        return  # Überspringen und zur nächsten Seite gehen

    # Daten sammeln (Überschriften und Absätze)
    data = []
    for tag in soup.find_all(["h1", "h2", "h3", "p"]):
        if tag.name in ["h1", "h2", "h3"]:
            gewichtung = {"h1": 2.0, "h2": 1.8, "h3": 1.6}.get(tag.name, 1.0)
            data.append({
                "Überschrift": tag.get_text(strip=True),
                "Gewichtung": gewichtung,
                "Inhalt": ""  # Inhalt wird nachfolgend ergänzt
            })
        elif tag.name == "p" and data:
            # Paragraf gehört zur letzten Überschrift
            data[-1]["Inhalt"] += tag.get_text(strip=True) + " "

    # Daten zu Resultaten hinzufügen
    for item in data:
        if len(item["Inhalt"]) > 0:
            result.append({
                "Thema": item['Überschrift'],
                "Text": clean_text(item['Inhalt']),
                "Gewichtung": item["Gewichtung"]
            })
    
    # Alle Links auf der Seite finden und normalisieren
    for link in soup.find_all('a', href=True):
        href = link['href']
        next_url = urljoin(url, href)
        
        # URL normalisieren
        next_url = normalize_url(next_url)
        
        # Prüfen, ob es ein interner Link ist und nicht bereits besucht wurde
        if base_url in next_url and urlparse(next_url).netloc == urlparse(base_url).netloc:
            if next_url not in visited_links:
                crawl(next_url)

# Startpunkt für das Crawling
def text_result(web_url):
    crawl(web_url)
    return result