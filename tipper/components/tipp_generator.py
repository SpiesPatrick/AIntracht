
import google.generativeai as genai
import yaml
# from google.generativeai.types import HarmCategory
# import pythonmodules.config as config
from models import config
from services.datacon import Datacon
from services.prompt import Prompt


def get_bundesliga_tipps(conf: config.Config, prompt: Prompt):
    api_key = conf.gemini.api_key
    if not api_key:
        raise ValueError('GEMINI_API_KEY wurde nicht in der Config gefunden.')

    genai.configure(api_key=api_key)

    bot_model = conf.gemini.bot_model
    if not bot_model:
        raise ValueError('BOT-MODEL wurde nicht in der Config gefunden.')

    model = genai.GenerativeModel(bot_model)

    try:
        # Generiere den Prompt
        p = prompt.generate_prompt()
        if not p:
            raise NotImplementedError('Prompt wurde nicht generiert')

        response = model.generate_content(p)

        if not response.parts:
            raise ValueError(f'Antwort ist leer. Finish Reason: {response.candidates[0].finish_reason}')

        text = response.text.strip()

        if not text:
            raise ValueError('Antwort vom Modell war leer.')

        if text.startswith('```yaml'):
            text = text.strip('```yaml').strip()

        tipps = text

    except AttributeError:
        print('Konnte nicht auf .text zugreifen. Möglicherweise wurde die Anfrage blockiert.')
        print('Komplette Antwort:', response)
        raise ValueError('Kein valider Text in der Antwort gefunden.')
    except Exception as e:
        print(f'Ein unerwarteter Fehler ist aufgetreten: {e}')
        raise

    return tipps

def generate():
    try:
        conf = config.load_config()
    except e:
        print('Unable to load config')
        print(e)
        exit()

    datacon = Datacon(dbname=conf.postgres.db_name,
                      user=conf.postgres.user_name,
                      password=conf.postgres.password,
                      host=conf.postgres.host)
    prompt = Prompt()

    saison_year = prompt.get_saison_year()
    match_day = prompt.get_match_day()
    print('Saison %s and matchday %s', (saison_year, match_day))


    with datacon.connect() as con:
        cur = con.cursor()

        if datacon.match_day_already_exists(cur=cur, saison=saison_year, match_day=match_day):
            # @TODO Logging
            print('"Spieltag" in this saison already exists in database')
            exit()
        try:
            tipps = get_bundesliga_tipps(conf=conf, prompt=prompt)
            print(tipps)
            datacon.safe_match_day_into_db(cur=cur, tipps_string=tipps)

        except Exception as e:
            print('Skript konnte nicht erfolgreich ausgeführt werden: ')
            print(e)

def main():
    generate()

if __name__ == "__main__":
    main()
