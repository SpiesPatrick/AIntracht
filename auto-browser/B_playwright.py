
import re

import Config
import yaml
from playwright.sync_api import Page, expect


def main():
    test_example(Page)

def test_example(page: Page) -> None:
    SPIELTAG = 2

    E_MAIL = Config.User.e_mail
    PASSWORD = Config.User.password
    GROUPNAME = Config.Kicktipp.group_name
    SAISON_ID = Config.Kicktipp.saison_id

    page.goto("https://www.kicktipp.de/{GROUPNAME}/")
    page.get_by_role("link", name="").click()
    page.get_by_role("textbox", name="E-Mail").click()
    page.get_by_role("textbox", name="E-Mail").fill(E_MAIL)
    page.get_by_role("textbox", name="Passwort").click()
    page.get_by_role("textbox", name="Passwort").fill(PASSWORD)
    page.get_by_role("button", name="Anmelden").click()
    page.locator("iframe[title=\"SP Consent Message\"]").content_frame.get_by_role("button", name="Akzeptieren und weiter").click()
    # page.get_by_role("link", name="Tippabgabe").click()
    page.goto(f"https://www.kicktipp.de/{GROUPNAME}/tippabgabe?tippsaisonId={SAISON_ID}&spieltagIndex={SPIELTAG}")
    # page.locator("#spieltippForms_1447474418_heimTipp").click()
    page.locator("#spieltippForms_1447474418_heimTipp").fill("4")
    # page.locator("#spieltippForms_1447474418_gastTipp").click()
    page.locator("#spieltippForms_1447474418_gastTipp").fill("3")
    page.get_by_role("button", name="Tipps speichern").click()
    expect(page.get_by_role("paragraph")).to_contain_text("Die Tipps wurden erfolgreich gespeichert.")

# WHAT CHATTIE SAYS
# async def main():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)  # oder False zum Debuggen
#         page = await browser.new_page()

#         # 1. Login
#         await page.goto(f"https://www.kicktipp.de/{GRUPPE}/tippabgabe?tippsaisonId=3989016&spieltagIndex=1")
#         await page.fill("input[name=kennung]", USERNAME)
#         await page.fill("input[name=passwort]", PASSWORD)
#         await page.click("button[type=submit]")

#         # 2. Tippseite öffnen
#         await page.goto(f"https://www.kicktipp.de/{GRUPPE}/tippabgabe")

#         # 3. Tipps eintragen (hier müsstest du Mapping bauen)
#         for idx, ((spiel, (home, away))) in enumerate(TIPPS.items(), start=1):
#             await page.fill(f"input[name=match_{idx}_home]", str(home))
#             await page.fill(f"input[name=match_{idx}_away]", str(away))

#         # 4. Absenden
#         await page.click("button[type=submit]")

#         print("Tipps erfolgreich eingetragen ✅")
#         await browser.close()

# asyncio.run(main())




'''
STEPS

import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://www.kicktipp.de/buli-lgh/');
  await page.getByRole('link', { name: '' }).click();
  await page.getByRole('textbox', { name: 'E-Mail' }).click();
  await page.getByRole('textbox', { name: 'E-Mail' }).fill('ai-ntracht@gmx.de');
  await page.getByRole('textbox', { name: 'Passwort' }).click();
  await page.getByRole('textbox', { name: 'Passwort' }).fill('geD$Ms#J@3Fzip8ZgHy5');
  await page.getByRole('button', { name: 'Anmelden' }).click();
  await page.locator('iframe[title="SP Consent Message"]').contentFrame().getByRole('button', { name: 'Akzeptieren und weiter' }).click();
  await page.getByRole('link', { name: 'Tippabgabe' }).click();
  await page.getByRole('row', { name: '1. FC Heidenheim 1846 VfL' }).getByRole('cell').first().click();
  await page.locator('#spieltippForms_1447474405_heimTipp').click();
  await page.locator('#spieltippForms_1447474405_heimTipp').fill('0');
  await page.locator('#spieltippForms_1447474405_gastTipp').click();
  await page.locator('#spieltippForms_1447474405_gastTipp').fill('1');
  await page.getByRole('button', { name: 'Tipps speichern' }).click();
});



import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://www.kicktipp.de/buli-lgh/")
    page.get_by_role("link", name="").click()
    page.get_by_role("textbox", name="E-Mail").click()
    page.get_by_role("textbox", name="E-Mail").fill("ai-ntracht@gmx.de")
    page.get_by_role("textbox", name="Passwort").click()
    page.get_by_role("textbox", name="Passwort").fill("geD$Ms#J@3Fzip8ZgHy5")
    page.get_by_role("button", name="Anmelden").click()
    page.locator("iframe[title=\"SP Consent Message\"]").content_frame.get_by_role("button", name="Akzeptieren und weiter").click()
    page.get_by_role("link", name="Tippabgabe").click()
    page.locator("#spieltippForms_1447474418_heimTipp").click()
    page.locator("#spieltippForms_1447474418_heimTipp").click()
    page.locator("#spieltippForms_1447474418_heimTipp").fill("4")
    page.locator("#spieltippForms_1447474418_gastTipp").click()
    page.locator("#spieltippForms_1447474418_gastTipp").fill("3")
    page.get_by_role("button", name="Tipps speichern").click()
    expect(page.get_by_role("paragraph")).to_contain_text("Die Tipps wurden erfolgreich gespeichert.")

'''
