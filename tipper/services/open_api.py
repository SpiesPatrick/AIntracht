
from datetime import datetime

import requests
import yaml


class OpenApi:

    def __init__(self):
        self.match_data = self.get_match_data()
        self.year = self.get_saison_year()
        self.table = self.get_table()

    def get_match_day_data(self):
        '''
        return integer representing the next matchday
        '''
        response = self.match_data
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

    def get_saison_year(self):
        '''
        calculating the current saison year
        '''
        return datetime.now().year if datetime.now().month >= 7 else datetime.now().year - 1

    def get_match_day(self):
        '''
        get the current matchday
        '''
        response = self.match_data
        return response.json()[0]['group']['groupOrderID']

    def get_table(self):
        '''
        return yaml of the actual table situation
        '''
        table = self.get_bundesliga_table().json()
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
            for item in table
        ]
        return yaml.dump(data=reduced_data, indent=2)

    def get_match_data(self):
        return requests.get('https://api.openligadb.de/getmatchdata/bl1')

    def get_bundesliga_table(self, year=None):
        if year is None:
            year = self.year
        return requests.get(f'https://api.openligadb.de/getbltable/bl1/{year}')

    def main(self):
        pass

    if __name__ == '__main__':
        main()
