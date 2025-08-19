import json

from openai import OpenAI

client = OpenAI()

def get_bundesliga_tips(spieltag: int):

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

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    # Rohtext auslesen
    text = response.choices[0].message.content.strip()

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
