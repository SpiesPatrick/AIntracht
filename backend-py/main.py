
import google.generativeai as genai
import prompt
import yaml
from google.generativeai.types import HarmCategory

import pythonmodules.config as config


def get_bundesliga_tips():
    '''
    Holt Bundesliga-Tipps vom Gemini-Modell und gibt sie als JSON zurück.
    '''
    conf = config.load_config()

    api_key = conf.gemini.api_key
    if not api_key:
        raise ValueError('GEMINI_API_KEY wurde nicht in der Config gefunden.')

    genai.configure(api_key=api_key)

    bot_model = conf.gemini.bot_model
    if not bot_model:
        raise ValueError('BOT-MODEL wurde nicht in der Config gefunden.')

    model = genai.GenerativeModel(bot_model)

    try:
        p = prompt.generate_promt()
        if not p:
            raise NotImplementedError('Prompt wurde nicht generiert')

        response = model.generate_content(prompt.generate_promt())

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
    try:
        tips = get_bundesliga_tips()
        print(tips)
    except Exception as e:
        print('Skript konnte nicht erfolgreich ausgeführt werden: ')
        print(e)

if __name__ == "__main__":
    main()
    main()
