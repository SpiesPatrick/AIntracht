import psycopg2
from models import tipps


class Datacon:

    def __init__(self, dbname, user, password, host, port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        return  psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)

    def safe_match_day_into_db(self, cur, tipps_string):
        tipps_yaml = tipps.convert_yaml(tipps_string)
        saison = tipps_yaml.spiele.saison
        spieltag = tipps_yaml.spiele.spieltag
        begegnungen = tipps_yaml.spiele.begegnungen
        # self.create_saison_if_not_exists(cur, saison.jahr) # Macht dieser Bums hier überhaupt noch Sinn?
        cur.execute('''
            INSERT INTO aintracht.spiele (saison, spieltag)
            VALUES (%s, %s)
            ON CONFLICT (saison, spieltag) DO NOTHING;
        ''', (saison, spieltag))

        for begegnung in begegnungen:
            cur.execute('''
                INSERT INTO aintracht.begegnungen (
                    heim_mannschaft,
                    gast_mannschaft,
                    heim_tore,
                    gast_tore,
                    saison,
                    spieltag
                ) VALUES(%s, %s, %s, %s, %s, %s);
            ''',
            (
                begegnung.heim_mannschaft,
                begegnung.gast_mannschaft,
                begegnung.heim_tore,
                begegnung.gast_tore,
                saison,
                spieltag
            ))

    def match_day_already_exists(self, cur, saison: int, match_day: int) -> bool:
        '''
        Überprüfe ob bereits ein Tipp in der Datenbank hinterlegt wurde.
        '''
        cur.execute('''
        SELECT EXISTS (
            SELECT 1 FROM aintracht.spiele spiele
            WHERE spiele.saison = %s
            AND spiele.spieltag = %s
        );
        ''', (saison, match_day))
        exists = cur.fetchone()[0]
        return exists
