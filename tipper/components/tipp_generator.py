import logging

import google.generativeai as genai
from models import config
from services.datacon import Datacon
from services.open_api import OpenApi
from services.prompt import Prompt

logger = logging.getLogger(__name__)

def get_bundesliga_tipps(conf: config.Config, prompt: Prompt, saison: int, match_day: int):
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

        tipps = 'spiele:\n' \
        f'  saison: {saison}\n' \
        f'  spieltag: {match_day}\n' \

        tipps = tipps + '  ' + text

    except AttributeError:
        logger.error('Konnte nicht auf .text zugreifen. Möglicherweise wurde die Anfrage blockiert.')
        logger.error('Komplette Antwort:', response)
        raise ValueError('Kein valider Text in der Antwort gefunden.')
    except Exception as e:
        logger.error('Ein unerwarteter Fehler ist aufgetreten:')
        logger.error(e)
        raise

    return tipps

def generate():
    try:
        conf = config.load_config()
    except e:
        logger.error('Unable to load config')
        logger.error(e)
        exit()

    datacon = Datacon(dbname=conf.postgres.db_name,
                      user=conf.postgres.user_name,
                      password=conf.postgres.password,
                      host=conf.postgres.host)
    prompt = Prompt()
    open_api = OpenApi()

    saison_year = open_api.get_saison_year()
    match_day = open_api.get_match_day()
    logger.info(f'Saison year: {saison_year} | Matchday: {match_day}')

    with datacon.connect() as con:
        cur = con.cursor()

        if datacon.match_day_already_exists(cur=cur, saison=saison_year, match_day=match_day):
            # @TODO Logging
            logger.info('"Spieltag" in this saison already exists in database')
            return
        try:
            tipps = get_bundesliga_tipps(conf=conf, prompt=prompt, saison=saison_year, match_day=match_day)
            logger.debug(f'Tipps: {tipps}')
            datacon.safe_match_day_into_db(cur=cur, tipps_string=tipps)

        except Exception as e:
            logger.error('Skript konnte nicht erfolgreich ausgeführt werden: ')
            logger.error(e)

def main():
    generate()

if __name__ == "__main__":
    main()
