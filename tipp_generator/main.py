
import google.generativeai as genai
import yaml
from google.generativeai.types import HarmCategory

import pythonmodules.config as config
from pythonmodules import config
from tipp_generator.datacon import Datacon
from tipp_generator.prompt import Prompt


def get_bundesliga_tips(conf: config.Config, prompt: Prompt):
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

        # tips = yaml.dump(data=text, indent=2)
        tips = text

    except AttributeError:
        print('Konnte nicht auf .text zugreifen. Möglicherweise wurde die Anfrage blockiert.')
        print('Komplette Antwort:', response)
        raise ValueError('Kein valider Text in der Antwort gefunden.')
    except Exception as e:
        print(f'Ein unerwarteter Fehler ist aufgetreten: {e}')
        raise

    return tips

def safe_bundesliga_tips_into_db(tips):
    # @TODO continue here
    pass

def main():

    datacon = Datacon()
    prompt = Prompt()

    try:
        conf = config.load_config()
    except:
        print('Unable to load config')
        exit()

    try:
        conn = datacon.connection(dbname=conf.postgres.db_name, user=conf.postgres.user_name, password=conf.postgres.password, host=conf.postgres.host)
    except:
        print('Unable to connect to database')
        exit()

    saison_year = prompt.get_saison_year()
    match_day = prompt.get_match_day()

    with conn.cursor() as cur:
        if datacon.check_if_spieltag_and_saison_already_exists(cur=cur, jahr=saison_year, spieltag=match_day):
            # @TODO Logging
            print('"Spieltag" in this saison already exists in database')
            exit()
        try:
            tips = get_bundesliga_tips(conf=conf)
            print(tips)
            safe_bundesliga_tips_into_db(tips)
        except Exception as e:
            print('Skript konnte nicht erfolgreich ausgeführt werden: ')
            print(e)

if __name__ == "__main__":
    main()
    main()
