import psycopg2
from models import tipps
from psycopg2.extras import RealDictCursor


class Datacon:

    def __init__(self, dbname, user, password, host, port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        return  psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            cursor_factory=RealDictCursor)

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

    def get_current_matches(self, cur, saison: int, match_day: int):
        '''
        Hole die Daten des Spieltags
        '''
        cur.execute('''
        SELECT * FROM aintracht.begegnungen b
        WHERE b.saison = %s AND b.spieltag = %s;
        ''', (saison, match_day))
        tipps = cur.fetchall()
        return tipps

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
        exists = cur.fetchone()['exists']
        return exists

    def match_day_already_tipped(self, cur, saison: int, match_day: int) -> bool:
        '''
        Überprüfe ob bereits getippt wurde für den hinterlegten Spieltag
        '''
        cur.execute('''
        SELECT spiele.getippt
        FROM aintracht.spiele spiele
        WHERE spiele.saison = %s
        AND spiele.spieltag = %s
        LIMIT 1;
        ''', (saison, match_day))
        tipped = cur.fetchone()['getippt']
        return tipped

    def set_match_day_tipped(self, cur, saison: int, match_day: int):
        '''
        Markiere den aktuellen Spieltag als getippt
        '''
        cur.execute('''
        UPDATE aintracht.spiele SET getippt=true
        WHERE saison = %s AND spieltag = %s;
        ''', (saison, match_day))
