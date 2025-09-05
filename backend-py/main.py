import os

import google.generativeai as genai
import prompt
import yaml
from google.generativeai.types import HarmCategory

api_key=os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY wurde nicht in den Umgebungsvariablen gefunden.")

genai.configure(api_key=api_key)


def get_bundesliga_tips(spieltag: int):
    """
    Holt Bundesliga-Tipps vom Gemini-Modell und gibt sie als JSON zurück.
    """

    model = genai.GenerativeModel('gemini-2.0-flash')

    try:
        response = model.generate_content(prompt.generate_promt())

        if not response.parts:
            raise ValueError(f"Antwort ist leer. Finish Reason: {response.candidates[0].finish_reason}")

        text = response.text.strip()

        if not text:
            raise ValueError("Antwort vom Modell war leer.")

        if text.startswith("```yaml"):
            text = text.strip("```yaml").strip()

        # tips = yaml.dump(data=text, indent=2)
        tips = text

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
        print(tips)
    except Exception as e:
        print("\nSkript konnte nicht erfolgreich ausgeführt werden.")
        print(e)

if __name__ == "__main__":
    main()
