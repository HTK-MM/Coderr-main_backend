# Coderr Backend API
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/HTK-MM/CoderrBackend/main/README.md) [![de](https://img.shields.io/badge/lang-de-yellow.svg)](https://github.com/HTK-MM/CoderrBackend/main/README.de.md)


## Beschreibung

**Coderr** Projekt ist eine API, die mit Django und Django REST Framework entwickelt wurde, um Benutzer, Angebote, Bestellungen und Bewertungen auf einer Geschäftsplattform zu verwalten.

## Verwendete Technologien

- Python 3.x

- Django 5.1.6
  
- Django REST Framework 3.15.2

- SQLite 


## Installation

1. Klonen Sie das Repository:
   ```bash
   git clone https://github.com/HTK-MM/CoderrBackend/.git
    cd projekt
   ```

2. Erstellen und aktivieren Sie eine virtuelle Umgebung:
    ````bash    
    python -m venv venv
       source venv/bin/activate  # Unter Windows: venv\Scripts\activate
    ````

3. Installieren Sie die Abhängigkeiten:

    ````bash 
    pip install -r requirements.txt
    ````

4. Konfigurieren Sie die Datenbank und führen Sie Migrationen durch:

    ````bash 
    python manage.py migrate
    ````

5. Erstellen Sie einen Superuser (optional für den Zugriff auf das Admin-Panel):
    ````bash 
    python manage.py createsuperuser
    ````

6. Starten Sie den Entwicklungsserver:
    ````bash 
    python manage.py runserver
    ````

7. Frontend Einrichten: In der Datei shared/scripts/config.js ändern:
    ````bash
   const GUEST_LOGINS = {
        customer : {
            username: 'guest_customer'
        },
        business : {
            username: 'guest_business'     
        }
    }
    ````

## API Endpunkte

### :small_blue_diamond: Baseinformation

-   ````**GET /base-info/**```` - Statistische Informationen

### :small_blue_diamond: Profile

-   ````**GET /profiles/customer/**```` - Liste alle Kundenprofile
-   ````**GET /profiles/business/**```` - Liste alle Geschäftsprofile   
-   ````**GET /profile/<int:pk>**````    - Details eines spezifischen Benutzer
-   ````**PATCH /profile/<int:pk>**````  - Aktualisierung Details eines spezifischen Benutzer

### :small_blue_diamond: Authentifizierung

- ````**POST /login/**```` - Benutzer Anmeldung 

- ````**POST /registration/**```` - Benutzerregistrierung
  
### :small_blue_diamond: Offers

-   ````**GET /offers/**```` - Auflistung von Angeboten mit Filter- und Suchmöglichkeiten.
-   ````**POST /offers/**```` - Erstellung eines neuen Angebots.
-   ````**GET /offers/{id}**```` - Details eines spezifichen Angebots.
-   ````**PATCH /offers/{id}**```` - Aktualisierung eines spezifichen Angebots.
-   ````**DELETE /offers/{id}**```` - Löschen eines spezifichen Angebots.
-   ````**GET /offerdetails/{id}**```` - Details eines spezifischen Angebotsdetails.

### :small_blue_diamond: Orders

-    ````**GET /orders/**```` - Auflistung von Bestellungen des angemeldeten Benutzer.
-    ````**POST /orders/**```` - Erstellung einer neuen Bestellung im Bezug eines Angebot.
-    ````**GET /orders/{id}**```` - Details einer spezifichen Bestellung.
-    ````**PATCH /orders/{id}**```` - Aktualisierung des Status einer spezifichen Bestellung.
-    ````**DELETE /orders/{id}**```` - Löschen einer spezifichen Bestellung.
-    ````**GET /order-count/<business_user_id>/**```` - Anzahl der Bestellungen eines Geschäftprofil.
-    ````**GET /completed-order-count/<business_user_id>/**```` - Anzahl der abgeschlossenen Bestellungen eines  Geschäftprofil


### :small_blue_diamond: Reviews

-    ````**GET /reviews/**```` - Auflistung von Bewertungen.
-    ````**POST /reviews/**```` - Erstellung einer neuen Bewertung.    
-    ````**GET /reviews/{id}**```` - Details einer spezifichen Bewertung.
-    ````**PATCH /reviews/{id}**```` - Aktualisierung einer spezifichen Bewertung.
-    ````**DELETE /reviews/{id}**```` - Löschen einer spezifichen Bewertung.

## Tests

Um automatisierte Tests auszuführen:
```bash
python manage.py test
````


