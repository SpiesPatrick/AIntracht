import json
import os

import google.generativeai as genai

# TODO get API KEY and make global var
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_bundesliga_tips(spieltag: int):

    model = genai.GenerativeModel("gemini-2.5-pro")

    prompt = f"""
    Gib die Tipps für den {spieltag}. Spieltag der 1. Fußball-Bundesliga
    im JSON-Format zurück.
    Format:
    {{
      "TeamA vs TeamB": "ToreA:ToreB",
      ...
    }}
    Keine Erklärungen, nur JSON.
    """

    response = model.generate_content(prompt)
    text = response.text.strip()

    # JSON parsen
    try:
        tips = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError("Antwort war kein valides JSON:\n" + text)

    return tips


def main():
    tips = get_bundesliga_tips(spieltag=1)
    print(json.dumps(tips, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
