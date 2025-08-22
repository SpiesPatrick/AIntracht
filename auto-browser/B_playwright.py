import asyncio

from playwright.async_api import async_playwright

USERNAME = "dein_username"
PASSWORD = "dein_passwort"
GRUPPE = "buli-lgh"
# URL_TIPPABGABE = "https://www.kicktipp.de/buli-lgh/tippabgabe?tippsaisonId=3989016&spieltagIndex={SPIELTAG}"

# TODO Tippsformat überarbeiten
TIPPS = {
    "Bayern vs Dortmund": (2, 1),
    "Leipzig vs Stuttgart": (1, 1),
}

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # oder False zum Debuggen
        page = await browser.new_page()

        # 1. Login
        await page.goto(f"https://www.kicktipp.de/{GRUPPE}/")
        await page.fill("input[name=kennung]", USERNAME)
        await page.fill("input[name=passwort]", PASSWORD)
        await page.click("button[type=submit]")

        # 2. Tippseite öffnen
        await page.goto(f"https://www.kicktipp.de/{GRUPPE}/tippabgabe")

        # 3. Tipps eintragen (hier müsstest du Mapping bauen)
        for idx, ((spiel, (home, away))) in enumerate(TIPPS.items(), start=1):
            await page.fill(f"input[name=match_{idx}_home]", str(home))
            await page.fill(f"input[name=match_{idx}_away]", str(away))

        # 4. Absenden
        await page.click("button[type=submit]")

        print("Tipps erfolgreich eingetragen ✅")
        await browser.close()

asyncio.run(main())
