
import time

from models import config, tipps
from playwright.sync_api import expect, sync_playwright
from services.datacon import Datacon
from services.prompt import Prompt


def send():
    try:
        conf = config.load_config()
    except e:
        print('Unable to load config: Abort')
        print(e)
        exit()

    datacon = Datacon(dbname=conf.postgres.db_name,
                      user=conf.postgres.user_name,
                      password=conf.postgres.password,
                      host=conf.postgres.host)

    with sync_playwright() as p, datacon.connect() as con:
        cur = con.cursor()

        # Load config
        try:
            E_MAIL = conf.user.e_mail
            PASSWORD = conf.user.password
            GROUPNAME = conf.kicktipp.group_name
            SAISON_ID = conf.kicktipp.saison_id
            HEADLESS = conf.kicktipp.headless
        except Exception as e:
            print('Failed to load config')
            return

        prompt = Prompt()

        saison_year = prompt.get_saison_year()
        match_day = prompt.get_match_day()

        if tipping_is_unnecessary(datacon=datacon, cur=cur, saison=saison_year, match_day=match_day):
            exit()
        browser = p.chromium.launch(headless=HEADLESS) # True =^ unsichtbar
        page = browser.new_page()

        # Load Tipps

        matches = datacon.get_current_matches(cur=cur, saison=saison_year, match_day=match_day)
        try:
            tipps_ = tipps.form_yaml(matches)
        except Exception as e:
            print('Failed to load tipps')
            return

        print(tipps_)
        SPIELE = max(tipps_.saison.spiele, key=lambda s: s.spieltag)
        SPIELTAG = SPIELE.spieltag
        print(f'current spieltag is {SPIELTAG}')

        page.goto(f'https://www.kicktipp.de/{GROUPNAME}/')

        '''
        1) Login
        '''
        page.get_by_role('link', name='').click()
        page.get_by_role('textbox', name='E-Mail').click()
        page.get_by_role('textbox', name='E-Mail').fill(E_MAIL)
        page.get_by_role('textbox', name='Passwort').click()
        page.get_by_role('textbox', name='Passwort').fill(PASSWORD)
        page.get_by_role('button', name='Anmelden').click()

        '''
        2) Navigate to Tipppage, depending on SPIELTAG
        '''
        time.sleep(1)
        try:
            page.locator("iframe[title=\"SP Consent Message\"]").content_frame.get_by_role("button", name="Akzeptieren und weiter").click()
        except Exception:
            print('No I-Frame found')
        # page.get_by_role("link", name="Tippabgabe").click()
        page.goto(f'https://www.kicktipp.de/{GROUPNAME}/tippabgabe?tippsaisonId={SAISON_ID}&spieltagIndex={SPIELTAG}')

        time.sleep(1)
        try:
            page.locator("iframe[title=\"SP Consent Message\"]").content_frame.get_by_role("button", name="Akzeptieren und weiter").click()
        except Exception:
            print('No I-Frame found')

        '''
        3) Filling the tips
        '''
        rows = page.locator('table#tippabgabeSpiele tbody tr.datarow' )

        count = rows.count()

        for i in range(count):
            row = rows.nth(i)
            heim = row.locator('.nw.cell.col1').inner_text()
            gast = row.locator('.nw.cell.col2').inner_text()

            '''
            TODO hier muss ich die Tipps/Tore aus meinem YAML auslesen
            und richtig definieren
            '''
            tore_heim = None
            tore_gast = None

            for match in SPIELE.begegnungen:
                if match.heim_mannschaft == heim and match.gast_mannschaft == gast:
                    tore_heim = match.heim_tore
                    tore_gast = match.gast_tore
                    pass

            if tore_heim == None or tore_gast == None:
                print(f'Could not match team for ${heim} or ${gast}')
                return

            row.locator('input[name*="heimTipp"]').fill(str(tore_heim))
            row.locator('input[name*="gastTipp"]').fill(str(tore_gast))

        '''
        4) Submit und check if saved
        '''
        page.get_by_role('button', name='Tipps speichern').click()
        expect(page.get_by_role('paragraph')).to_contain_text([
            'Die Tipps wurden erfolgreich gespeichert.',
            'Es wurden keine Änderungen gespeichert! Es wurden die gleichen Daten übermittelt, die bereits gespeichert sind.'
        ])
        print('Tipping was successfull')

def tipping_is_unnecessary(datacon: Datacon, cur, saison, match_day):
    if not datacon.match_day_already_exists(cur=cur, saison=saison, match_day=match_day):
        print('No matchday in database')
        return True
    if datacon.match_day_already_tipped(cur=cur, saison=saison, match_day=match_day):
        print('Already tipped for current matchday')
        return True
    return False

def sortBySpieltag(e):
  return e.spieltag

def main():
    send()

if __name__ == '__main__':
    main()
