import yaml
from services.open_api import OpenApi


class Prompt:

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

        return f'Gib mir bitte die Tipps für den {match_day}. Spieltag der 1. Bundesliga im YAML-Format.\n' \
                '\n' \
                'Das YAML soll so aufgebaut sein:\n' \
                '\n' \
                'begegnungen:\n' \
                '  - heim_mannschaft: "FC Bayern München" # Name der Heimmannschaft\n' \
                '    gast_mannschaft: "Werder Bremen" # Name der Gastmannschaft\n' \
                '    heim_tore: 0 # Unbedingt als Integer angeben!\n' \
                '    gast_tore: 2 # Unbedingt als Integer angeben!\n' \
                '  - ...\n' \
                '\n' \
                'Die aktuelle Tabelle der 1. Bundesliga sieht wie folgt aus (YAML-Format):\n' \
            f'{table}\n' \
                '\n' \
            f'Folgende Begegnungen gibt es am {match_day}. Spieltag:\n' \
                '\n' \
            f'{match_day_games}\n' \
                'Die sollte dir dazu dienen, die Leistungen der Teams einzuschätzen.\n' \
                '\n' \
                'Bitte verwende die Namen in der folgenden Liste und ersetze gegebenenfalls den Namen (keine Abweichungen, keine Kürzungen):\n' \
                'teams:\n' \
            f'{team_names}\n' \
                'Wichtige Punkte:\n' \
                '- Alle Spiele des Spieltags müssen enthalten sein.\n' \
                '- Team-Namen exakt so wie oben in der Liste (keine Variationen, egal was in der Tabelle oder im Match-Day steht!!!).\n' \
                '\n' \

def main():
    prompt_class = Prompt()
    prompt = prompt_class.generate_prompt()
    print(prompt)

if __name__ == '__main__':
    main()
