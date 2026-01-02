# ProWywóz 0.4.0

## -- PL --

### O aplikacji
Aplikacja służy do generowania kalendarza odbioru odpadów na terenie Bydgoszczy.
Dostępne wyszukiwarki:
- usługa świadczona przez MKUO ProNatura Sp z o.o. w Bydgoszczy
- usługa świadczona przez PUK CORIMP Sp z o.o. w Bydgoszczy (wersja beta)

### Pobieranie aplikacji
Aplikację przetestowano w Pythonie w wersji 3.13 i jest ona zalecana do działania. W przypadku starszych wersji Pythona nie ma 100% gwarancji.

- Pobierz projekt z GitHuba:
```
git clone https://github.com/odziom91/ProWywoz.git
```

- Utwórz środowisko wirtualne (opcjonalnie):
```
pip install virtualenv
python -m venv .venv
source .venv\bin\activate
```

- Zainstaluj wymagane moduły przez pip:
```
pip install -r requirements.txt
```

- Uruchom aplikację:
```
python ./prowywoz.py
```

### Jak działa aplikacja?
Po uruchomieniu aplikacji wystarczy wybrać usługodawcę (dostępne: ProNatura oraz CORIMP), ulicę oraz numer budynku.
Po kliknięciu na przycisk "Pobierz plik PDF" aplikacja wyśle żądanie do serwera, po czym zostanie pobrany wygenerowany plik PDF z harmonogramem odbioru odpadów.

### Po co powstała ta aplikacja?
W sumie "dla zabawy" - to bardziej "demo" możliwości dla GTK4 oraz Libadwaita.

### Co pozostało do zrobienia?
- uzupełnienie aplikacji o funkcję utworzenia pliku kalendarza dla wywozu odpadów w formacie *.ics
- mnóstwo poprawek w działaniu
- wkrótce obsługa wyszukiwarki Remondis

## -- EN --

### About the App
This app helps generate a waste collection calendar for Bydgoszcz.
Available search engines:
- service provided by MKUO ProNatura Sp. z o.o. in Bydgoszcz
- service provided by PUK CORIMP Sp. z o.o. in Bydgoszcz (beta version)

### Downloading the App
The application was tested with Python version 3.13 and is recommended for use with it. For older Python versions, there is no 100% guarantee of compatibility.

- Download the project from GitHub:
```
git clone https://github.com/odziom91/ProWywoz.git
```

-Create a virtual environment (optional):
```
pip install virtualenv
python -m venv .venv
source .venv\bin\activate
```

- Install the required modules via pip:
```
pip install -r requirements.txt
```

- Run the application:
```
python ./prowywoz.py
```

### How does the App work?
After starting the app, simply select service provider, street and building number.
Click the "Pobierz plik PDF" button, and the app will send a request to the server. It will download a generated PDF file with the waste collection schedule.

### Why was this app created?
Basically "for fun" - it is more of a "demo" to show the possibilities of GTK4 and Libadwaita.

### What is left to do?
- add a feature to create a calendar file for waste collection in *.ics format
- lots of fixes and improvements
- search engine for Remondis coming soon