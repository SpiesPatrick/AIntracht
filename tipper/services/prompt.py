import google.generativeai as genai
import yaml
from models import config
from services.open_api import OpenApi

class Prompt:

    def __init__(self):
        conf = config.load_config()
        self.api_key = conf.gemini.api_key
        self.bot_model = conf.gemini.bot_model

    def get_response(self, prompt):
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.bot_model)
        response = model.generate_content(prompt)
        return response.text.strip()


    def get_team_names(self):
        '''
        return string with all team names, the way I want (and need) it
        '''
        return  '  - "Hamburger SV"\n' \
                '  - "FC St. Pauli"\n' \
                '  - "RB Leipzig"\n' \
                '  - "1. FC Heidenheim 1846"\n' \
                '  - "VfB Stuttgart"\n' \
                '  - "Bor. Mönchengladbach"\n' \
                '  - "Werder Bremen"\n' \
                '  - "Bayer 04 Leverkusen"\n' \
                '  - "1899 Hoffenheim"\n' \
                '  - "Eintracht Frankfurt"\n' \
                '  - "FC Augsburg"\n' \
                '  - "FC Bayern München"\n' \
                '  - "VfL Wolfsburg"\n' \
                '  - "FSV Mainz 05"\n' \
                '  - "Borussia Dortmund"\n' \
                '  - "1. FC Union Berlin"\n' \
                '  - "1. FC Köln"\n' \
                '  - "SC Freiburg"\n' \

    def generate_prompt(self):
        '''
        return the complete prompt
        '''
        api = OpenApi()

        match_day_data = api.get_match_day_data()
        match_day = match_day_data.get('spieltag')
        match_day_games = yaml.dump(data=match_day_data.get('begegnungen'), indent=2)
        team_names = self.get_team_names()
        table = api.table

        return f'''
***
Deine Aufgabe ist es, den {match_day}. Spieltag der 1. Bundesliga zu tippen.
Erstelle möglichst realistische Ergebnisse.
***

***
Nutze für deine Einschätzung insbesondere:

- die aktuelle Tabellenposition
- Heimvorteil
- bisherige Saisonleistungen
- Offensiv- und Defensivstärke
- die aktuelle Form der Mannschaften, sofern bekannt

Überraschungen sind erlaubt, sollten aber plausibel sein.
***

***
Die aktuelle Tabelle der Bundesliga:

{table}
***

***
Am {match_day}. Spieltag finden folgende Begegnungen statt:

{match_day_games}
***

***
Verwende in deiner Ausgabe ausschließlich die folgenden Teamnamen.

Falls Mannschaften in der Tabelle oder den Begegnungen anders geschrieben sind,
ersetze sie durch den entsprechenden Namen aus dieser Liste.

teams:
{team_names}
***

***
Gib ausschließlich gültiges YAML zurück.

Das YAML muss exakt folgende Struktur besitzen:

begegnungen:
  - heim_mannschaft: "FC Bayern München"
    gast_mannschaft: "Werder Bremen"
    heim_tore: 2
    gast_tore: 1
  - heim_mannschaft: "..."
    gast_mannschaft: "..."
    heim_tore: 0
    gast_tore: 0
***

***
Regeln:

- Alle Begegnungen des Spieltags müssen enthalten sein.
- Jede Begegnung darf genau einmal vorkommen.
- Heim- und Gastmannschaft dürfen nicht vertauscht werden.
- Die Mannschaftsnamen müssen exakt der oben angegebenen Liste entsprechen.
- heim_tore und gast_tore müssen Integer sein.
- Es dürfen keine weiteren Felder ausgegeben werden.
- Gib ausschließlich das YAML zurück.
- Gib keine Erklärungen.
- Verwende keine Markdown-Codeblöcke.
***
'''

def main():
    prompt_class = Prompt()
    prompt = prompt_class.generate_prompt()
    print(prompt)
    response = prompt_class.get_response(prompt)
    print(response)

if __name__ == '__main__':
    main()
