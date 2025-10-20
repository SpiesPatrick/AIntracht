import psycopg2

from pythonmodules import tipps


def connection(dbname, user, password, host):
    return  psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=5432)

def match_day_is_already_tipped(cur, spieltag):
    cur.execute('SELECT bereits_getippt FROM aintracht.spiele WHERE spieltag = %s', (spieltag,))
    return cur.fetchone()[0]

def safe_match_day_into_db(cur, tips_string):
    tips_yaml = tipps.convert_yaml(tips_string)
    saison = tips_yaml.saison
    saison_id = get_or_create_saison(cur, saison.jahr)

def get_or_create_spieltag(cur, saison_id: int, spieltag: int) -> int:
    '''
    Holt die ID eines Spieltags oder erstellt diese, falls noch nicht vorhanden.
    Gibt die ID als int zurück.
    '''

def get_or_create_saison(cur, jahr: str) -> int:
    '''
    Holt die ID einer Saison oder erstellt sie, falls noch nicht vorhanden.
    Gibt die ID als int zurück.
    '''
    cur.execute('''
        INSERT INTO aintracht.saison (jahr)
        VALUES (%s)
        ON CONFLICT (jahr) DO UPDATE SET jahr = EXCLUDED.jahr
        RETURNING id;
    ''', (jahr,))
    saison_id = cur.fetchone()[0]
    return saison_id

def check_if_spieltag_and_saison_already_exists(cur, jahr: str, spieltag: int) -> bool:
    '''
    Überprüfe ob bereits ein Tipp in der Datenbank hinterlegt wurde.
    '''
    cur.execute('''
    SELECT EXISTS (
        SELECT 1 FROM aintracht.spiele spiele
        JOIN aintracht.saison saison ON spiele.saison_id = saison.id
        WHERE saison.jahr = %s
        AND spiele.spieltag = %s
    );
    ''', (jahr, spieltag))
    exists = cur.fetchone()[0]
    return exists

    # cur.execute("SELECT heim, gast, tipp_heim, tipp_gast FROM tipps WHERE spiel_id=%s", (1447474424,))
    # row = cur.fetchone()




    # conn = psycopg2.connect("dbname=test user=postgres")

    # # Open a cursor to perform database operations
    # cur = conn.cursor()

    # # Execute a command: this creates a new table
    # cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

    # # Pass data to fill a query placeholders and let Psycopg perform
    # # the correct conversion (no more SQL injections!)
    # cur.execute('INSERT INTO test (num, data) VALUES (%s, %s)', (123, 'datatata'))

    # # Query the database and obtain data as Python objects
    # cur.execute("SELECT * FROM test;")
    # cur.fetchone()
    # (1, 100, "abc'def")

    # # Make the changes to the database persistent
    # conn.commit()    # conn.commit()
    # # Make the changes to the database persistent
    # conn.commit()    # conn.commit()
    # conn.commit()    # conn.commit()
