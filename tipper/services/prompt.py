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
Deine Rolle ist es, den kommenden Spieltag in der Deutschen Bundesliga zu tippen.
***

***
Der kommende Spieltag ist der {match_day}. Spieltag der 1. Bundesliga der Herren
und es finden folgende Begegnungen statt:
{match_day_games}
***

***
Zur Orientierung folgt die aktuelle Tabelle der 1. Bundesliga:
{table}
***

***
Bitte verwende die Namen in der folgenden Liste und matche gegebenenfalls den Namen (keine Abweichungen, keine Kürzungen):
{team_names}
***

***
Deinen Tipp generierst du bereits als fertigen PostreSQL-Befehl, in folgender Form:

INSERT INTO aintracht.begegnungen (id, heim_mannschaft, gast_mannschaft, heim_tore, gast_tore, saison, spieltag)
VALUES(nextval('aintracht.begegnungen_id_seq'::regclass), '', '', 0, 0, 0, 0);
***


------------------------------------
Gib mir bitte die Tipps für den {match_day}. Spieltag der 1. Bundesliga im YAML-Format.

Das YAML soll so aufgebaut sein:

begegnungen:
  - heim_mannschaft: "FC Bayern München" # Name der Heimmannschaft
    gast_mannschaft: "Werder Bremen" # Name der Gastmannschaft
    heim_tore: 0 # Unbedingt als Integer angeben!
    gast_tore: 2 # Unbedingt als Integer angeben!
  - ...

Die aktuelle Tabelle der 1. Bundesliga sieht wie folgt aus (YAML-Format):
{table}

Folgende Begegnungen gibt es am {match_day}. Spieltag:
{match_day_games}

Die sollte dir dazu dienen, die Leistungen der Teams einzuschätzen.

Bitte verwende die Namen in der folgenden Liste und ersetze gegebenenfalls den Namen (keine Abweichungen, keine Kürzungen):
teams:
{team_names}

Wichtige Punkte:
- Alle Spiele des Spieltags müssen enthalten sein.
- Team-Namen exakt so wie oben in der Liste (keine Variationen, egal was in der Tabelle oder im Match-Day steht!!!).
'''

def main():
    prompt_class = Prompt()
    prompt = prompt_class.generate_prompt()
    print(prompt)
    response = prompt_class.get_response(prompt)
    print(response)

if __name__ == '__main__':
    main()
