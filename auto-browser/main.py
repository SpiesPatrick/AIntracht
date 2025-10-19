
import re
import time

import yaml
from playwright.sync_api import expect, sync_playwright

import pythonmodules.config as conf
import pythonmodules.tipps as gen_tipps


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # True =^ unsichtbar
        page = browser.new_page()


        # Load config
        try:
            config = conf.load_config()
            E_MAIL = config.user.e_mail
            PASSWORD = config.user.password
            GROUPNAME = config.kicktipp.group_name
            SAISON_ID = config.kicktipp.saison_id
        except Exception as e:
            print('Failed to load config')
            return

        # Load Tipps
        try:
            tipps = gen_tipps.load_tipp()
        except Exception as e:
            print('Failed to load tipps')
            return

        print(tipps)
        SPIELE = max(tipps.saison.spiele, key=lambda s: s.spieltag)
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
        expect(page.get_by_role('paragraph')).to_contain_text('Die Tipps wurden erfolgreich gespeichert.')


def sortBySpieltag(e):
  return e.spieltag

if __name__ == '__main__':
    main()
    main()
