
PROMPT_TEMPLATE = """
Gib mir bitte die Tipps für den {spieltag}. Spieltag der 1. Bundesliga im YAML-Format.

Die Struktur soll exakt so aussehen:

saison:
  - spieltag: "{spieltag}"
    begegnungen:
      - Heimmannschaft: "Tore"
        Gastmannschaft: "Tore"
    - ...

Wichtige Regeln:
- Alle 9 Spiele des Spieltags müssen enthalten sein.
- Nur YAML zurückgeben, keine zusätzlichen Erklärungen oder Kommentare.
- Alle Werte (auch Zahlen) immer in Anführungszeichen ("...").
"""

def get_prompt_for_spieltag(spieltag):
    return PROMPT_TEMPLATE.format(spieltag=spieltag)
