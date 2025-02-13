import re
import unicodedata

def clean_text(text):
    # Entferne phonetische Zeichen (z. B. [ˈa͡ɪfo͡ʊn])
    text = re.sub(r"\[.*?\]", "", text)

    # Unicode-Normalisierung (z. B. Entfernen von diakritischen Zeichen)
    text = unicodedata.normalize("NFKD", text)

    # Ersetze unnötige Bindestriche mit einem Leerzeichen oder entferne sie
    text = re.sub(r"(\w)- (\w)", r"\1\2", text)  # Setzt getrennte Wörter wieder zusammen
    text = re.sub(r"\b-\b", " ", text)  # Entfernt alleinstehende Bindestriche

    # Entferne doppelte oder unnötige Leerzeichen
    text = re.sub(r"\s+", " ", text).strip()

    return text

