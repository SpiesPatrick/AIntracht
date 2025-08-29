import json
import os

import google.generativeai as genai
from google.generativeai.types import HarmCategory
from prompt import get_prompt_for_spieltag

api_key=os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY wurde nicht in den Umgebungsvariablen gefunden.")

genai.configure(api_key=api_key)


def get_bundesliga_tips(spieltag: int):
    """
    Holt Bundesliga-Tipps vom Gemini-Modell und gibt sie als JSON zurück.
    """

    model = genai.GenerativeModel("gemini-2.5-pro")

    prompt = get_prompt_for_spieltag(spieltag=spieltag)

    try:
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.safety_types.HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.safety_types.HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.safety_types.HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.safety_types.HarmBlockThreshold.BLOCK_NONE,
        }

        response = model.generate_content(prompt, safety_settings=safety_settings)

        if not response.parts:
            raise ValueError(f"Antwort ist leer. Finish Reason: {response.candidates[0].finish_reason}")

        text = response.text.strip()

        if not text:
            raise ValueError("Antwort vom Modell war leer.")

        if text.startswith("```json"):
            text = text.strip("```json").strip()

        tips = json.loads(text)

    except (ValueError, json.JSONDecodeError) as e:
        print("Fehler beim Verarbeiten der Modell-Antwort.")
        print("Original-Antwort:", response.text)
        raise ValueError("Antwort war kein valides JSON oder konnte nicht gelesen werden.") from e
    except AttributeError:
        print("Konnte nicht auf .text zugreifen. Möglicherweise wurde die Anfrage blockiert.")
        print("Komplette Antwort:", response)
        raise ValueError("Kein valider Text in der Antwort gefunden.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        raise

    return tips


def main():
    try:
        tips = get_bundesliga_tips(spieltag=1)
        print(json.dumps(tips, indent=2, ensure_ascii=False))
    except Exception as e:
        print("\nSkript konnte nicht erfolgreich ausgeführt werden.")

if __name__ == "__main__":
    main()
