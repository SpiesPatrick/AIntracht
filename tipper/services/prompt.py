
import json
from datetime import datetime

import requests
import yaml


class Prompt:

    # def __init__(self):
    #     pass

    def get_saison_year():
        '''
        calculating the current saison year
        '''
        return datetime.now().year if datetime.now().month >= 7 else datetime.now().year - 1

    def get_match_day():
        '''
        get the current matchday
        '''
        response = requests.get('https://api.openligadb.de/getmatchdata/bl1')
        return response.json()[0]['group']['groupOrderID']

    def get_table(self):
        '''
        return a json or yaml (not sure yet) of the actual table situation
        '''
        year = self.get_saison_year()
        response = requests.get(f'https://api.openligadb.de/getbltable/bl1/{year}')
        data = response.json()
        reduced_data = [
            {
                'team': item.get('teamName'),
                'punkte': item.get('points'),
                'siege': item.get('won'),
                'niederlagen': item.get('lost'),
                'unentschieden': item.get('draw'),
                'tore_geschossen': item.get('goals'),
                'tore_gegner': item.get('opponentsGoals'),
                'tordifferenz': item.get('goalDiff')
            }
            for item in data
        ]
        return yaml.dump(data=reduced_data, indent=2)

    def get_match_day_data():
        '''
        return integer representing the next matchday
        '''
        response = requests.get('https://api.openligadb.de/getmatchdata/bl1')
        data = response.json()
        reduced_data = {
            'spieltag': data[0]['group']['groupOrderID'],
            'begegnungen': [
                {
                    'heim_mannschaft': item.get('team1').get('teamName'),
                    'gast_mannschaft': item.get('team2').get('teamName')
                }
                for item in data
            ]
        }
        return reduced_data

    def get_team_names():
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
        match_day_data = self.get_match_day_data()
        match_day = match_day_data.get('spieltag')
        match_day_games = yaml.dump(data=match_day_data.get('begegnungen'), indent=2)
        team_names = self.get_team_names()
        table = self.get_table()

        return f'Gib mir bitte die Tipps für den {match_day}. Spieltag der 1. Bundesliga im YAML-Format.\n' \
                '\n' \
                'Das YAML soll so aufgebaut sein:\n' \
                '\n' \
                'saison: 25 # Unbedingt als Integer angeben! Lautet die Saison "25/26", so nimmst du die kleinere Zahl, also 25 \n' \
                'spieltag: 3 # Unbedingt als Integer angeben!\n' \
                'begegnungen:\n' \
                '- heim_mannschaft: "FC Bayern München" # Name der Heimmannschaft\n' \
                '  gast_mannschaft: "Werder Bremen" # Name der Gastmannschaft\n' \
                '  heim_tore: 0 # Unbedingt als Integer angeben!\n' \
                '  gast_tore: 2 # Unbedingt als Integer angeben!\n' \
                '- ...\n' \
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

    def main(self):
        prompt = self.generate_prompt()
        print(prompt)

    if __name__ == '__main__':
        main()
        main()
