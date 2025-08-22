import requests
from bs4 import BeautifulSoup

USERNAME = "dein_username"
PASSWORD = "dein_passwort"
GRUPPE = "meine-tippgruppe"

# TODO Tippsformat überarbeiten
TIPPS = {
    "Bayern vs Dortmund": "2:1",
    "Leipzig vs Stuttgart": "1:1",
}

session = requests.Session()

# 1. Login-Seite laden → CSRF-Token finden
login_page = session.get("https://www.kicktipp.de/{}/".format(GRUPPE))
soup = BeautifulSoup(login_page.text, "html.parser")
csrf = soup.find("input", {"name": "csrfToken"})["value"]

# 2. Login-Request
login_payload = {
    "kennung": USERNAME,
    "passwort": PASSWORD,
    "csrfToken": csrf,
}
session.post(f"https://www.kicktipp.de/{GRUPPE}/login", data=login_payload)

# 3. Tippseite laden (Beispiel für Spieltag 1)
tipps_page = session.get(f"https://www.kicktipp.de/{GRUPPE}/tippabgabe")
soup = BeautifulSoup(tipps_page.text, "html.parser")

# 4. Tipp-Felder auslesen (hier musst du IDs/Names anpassen!)
payload = {"csrfToken": soup.find("input", {"name": "csrfToken"})["value"]}
payload.update({
    "match_1_home": 2,
    "match_1_away": 1,
    "match_2_home": 1,
    "match_2_away": 1,
})

# 5. Absenden
r = session.post(f"https://www.kicktipp.de/{GRUPPE}/tippabgabe", data=payload)
print("Tipps gesendet:", r.status_code)
