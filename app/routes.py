from flask import Blueprint, request, jsonify
from app.getcontext import get_context
from app.ask_ai.askollama import ask_ollama
from app.ask_ai.askopenai import ask_openai
import logging

bp = Blueprint("chatbot", __name__)

ask_open_ai = True

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)

@bp.route("/chat", methods=["POST"])
def chat():
    try:
        # Überprüfen, ob JSON-Daten gesendet wurden
        if not request.is_json:
            return jsonify({"error": "Invalid JSON format"}), 400
        
        data = request.get_json()
        user_message = data.get("text", "")
        web_url = data.get("url", "")

        # Eingabewert prüfen
        if not isinstance(user_message, str) or not user_message.strip():
            return jsonify({"error": "Message must be a non-empty string"}), 400

        # Suche relevante Inhalte im Kontext
        context = get_context(user_message,web_url)
        print(context)

        # Frage OpenRouter mit Timeout-Handling
        try:
            response = ask_openai(user_message, context) if ask_open_ai else ask_ollama(user_message, context)
        except TimeoutError:
            logging.error("Timeout bei der Anfrage an ask_ollama")
            return jsonify({"error": "Request timeout"}), 504
        except Exception as e:
            logging.error(f"Fehler bei ask_ollama: {e}")
            return jsonify({"error": "Internal server error"}), 500
        
        # Erfolgreiche Antwort zurückgeben
        return jsonify({"reply": response})

    except Exception as e:
        logging.error(f"Unbekannter Fehler: {e}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route("/test", methods=["GET"])
def test():
    try:
        return jsonify({"message": "Success!"}), 200
    except Exception as e:
        logging.error(f"Fehler bei ask_ollama: {e}")
        return jsonify({"error": "Invalid JSON format"}), 400
