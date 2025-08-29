
import re

import Config as conf
import yaml
from playwright.sync_api import expect, sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # True =^ unsichtbar
        page = browser.new_page()

        SPIELTAG = 2

        try:
            # Load config
            config = conf.load_config()
            E_MAIL = config.user.e_mail
            PASSWORD = config.user.password
            GROUPNAME = config.kicktipp.group_name
            SAISON_ID = config.kicktipp.saison_id
        except Exception as e:
            return

        page.goto('https://www.kicktipp.de/{GROUPNAME}/')

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
        try:
            page.locator("iframe[title=\"SP Consent Message\"]").content_frame.get_by_role("button", name="Akzeptieren und weiter").click()
        except Exception:
            print('No I-Frame found')
        # page.get_by_role("link", name="Tippabgabe").click()
        page.goto(f'https://www.kicktipp.de/{GROUPNAME}/tippabgabe?tippsaisonId={SAISON_ID}&spieltagIndex={SPIELTAG}')


        '''
        3) Filling the tips
        '''
        rows = page.locator('table#tippabgabeSpiele tr')

        for row in rows:
            heim = row.locator('.nw cell col1').inner_text()
            gast = row.locator('.nw cell col2').inner_text()

            '''
            TODO hier muss ich die Tipps/Tore aus meinem YAML auslesen
            und richtig definieren
            '''

            row.locator('input[name*="heimTipp"]').fill(tore_heim)
            row.locator('input[name*="gastTipp"]').fill(tore_gast)

        '''
        4) Submit und check if saved
        '''
        page.get_by_role('button', name='Tipps speichern').click()
        expect(page.get_by_role('paragraph')).to_contain_text('Die Tipps wurden erfolgreich gespeichert.')


if __name__ == '__main__':
    main()
