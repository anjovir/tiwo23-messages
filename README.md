# Keskustelusovellus

Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Sovelluksen ominaisuuksia:

   1. Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
   2. Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
   3. Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
   4. Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
   5. Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
   6. Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
   7. Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
   8. Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

Valmiina:
   - Kohdat 1-7

Testaus:
   - kopioi repositorio
   - luo .env tiedosto, sinne tulee luoda SECRET_KEY esim. komennolla python3 -> import secrets -> secret.token_hex(16)
   - lisäksi sinne tulee määrittää tietokannan osoite, esim. DATABASE_URL="postgresql:///your_db_name"
   - Admin-käyttäjän salasana tulee myös lisä .env-tiedostoon, kohtaan ADMIN_PASSWORD="oma_salasana"
   - venv-ympäristö käyttöön komennolla python3 -m venv venv -> source/bin/activate
   - aja pip install -r requirements.txt
   - luo tietokanta käyttäen sql-skeemaa: psql < schema.sql
   - testiympäristö käyttöön komennolla flask run


Versio 0.1:
   - käyttäjä pystyy kirjautumaan sivulle ja luomaan tunnuksen
   - käyttäjä pystyy luomaan keskustelun ja ensimmäisen postauksen siihen
   - index.html-sivulle nousee esiin general-keskustelualueen viimeisimmän viestin postausajankohta ja viestin kirjoittaja
   - istunnoissa on käytetty ympäristömuuttujia
   - tietokannan skeema on luotu
   - versionhallinta gitiin luotu
   - sivujen rakenne ja ulkoasu pitkälti luomatta
   - sivupohjassa ja rakenteessa hyödynnetään kurssimateriaaleja (kirjautuminen, istunnot, uuden tunnuksen luominen jne.)
   - https://github.com/hy-tsoha/tsoha-chat/tree/master

Versio 0.2:
   - muokattu pääsivua
   - luotu linkit eri aihealueiden sivuille ja luotu perussivustolle
   - poistettu threads.html-tiedosto
   - luotu listaus keskusteluista aihealueiden sisälle
   - lisätty css-tyylitiedosto ja määritelty mm. table-elementtejä
   - muokattu sql-skeemaa ja lisätty mm. aikaleimasarake threads-taulukkoon
   - siistitty koodia

Versio 0.2.1
   - korjattu alkutilanne, jossa tietokantaan ei ole lisätty viestejä
   - lisätty thread.html viestien näyttämistä varten
   - muokattu sivujen index.html ja general.html ulkoasua
   - lisätty sivulle general.html viestien määrän laskuri

Versio 0.2.2
   - lisätty siirtyminen keskusteluketjusta itse keskusteluun

Versio 0.2.3
   - lisätty mahdollisuus lähettää viesti keskusteluketjuun
   - päivitetty sivujen tekstejä

Versio 0.2.4
   - laajennettu viestimahdollisuus kaikkiin aihealueisiin

Versio 0.2.5
   - lisätty editointimahdollisuus viesteihin

Versio 0.2.6
   - lisätty mahdollisuus poistaa lähetetty viesti
   - muutettu skeeman luonnin järjestystä

Versio 0.2.6.1.
   - muokattu sivujen ulkoasua, siirretty nappien paikkaa

Versio 0.2.7.
   - lisätty mahdollisuus muokata keskustelun otsikkoa
   - lisätty myös delete nappi tälle, mutta ei funktiota

Versio 0.3
   - lisätty mahdollisuus deletoida keskusteluketju
   - muokattu SQL-skeemaa siten, että deletointi mahdollistuu
   - SQL-skeema pitäisi toimia paremmin setup-vaiheessa

Versio 0.3.1
   - luotu salasana vaihtosivu, tietoturva ei siinä vielä kunnossa

Versio 0.3.2
   - luotu huono tapa, jolla luodaan admin-käyttäjä, mikäli sitä ei ole jo luotu
   - ympäristömuuttuja määritetty admin-salasanalle

Versio 0.4
   - yksinkertaistettu sivurakennetta
   - poistettu erilliset staattiset eri aihealueiden sivut (general, politics, economy)
   - kaikki aihealueet generoituvat tietokannan sisällön perusteella
   - luotu tähän uusi topic.html sivu
   - hiottu ulkoasua

Versio 0.4.1
   - muokattu roolitauluja ja user tauluja, luotu yhteys
   - päivitetty metodit huomioiden taulurakenteen korjaukset
   - korjattu sivujen käyttöönottoon liittyviä bugeja

Versio 0.4.2
   - korjattu rekisteröitymiseen liittyvä bugi

Versio 0.4.3.
   - päivitetty keskusteluketjun luomiseen liittyvä toiminnallisuus

Versio 0.4.4
   - lisätty metodi, jolla tarkistetaan, onko käyttäjä admin-roolissa

Versio 0.4.5
   - lisätty adminille mahdollisuus luoda uusi keskusteluaihe ("topic") aloitussivulla

Versio 0.4.6
   - lisätty adminille mahdollisuus poistaa keskusteluaihe ("topic") aloitussivulla

Versio 0.4.7
   - lisätty yksinkertainen hakutoiminto pääsivulle

Versio 0.4.8
   - lisätty löydettyihin hakuihin linkit keskusteluketjuun
   - lisätty ilmoitus, mikäli haku ei tuota tulosta

Versio 0.4.9
   - korjattu csfr-haavoittuvuus

V 0.4.9.1
   - korjattu bugi, jossa näkyi väärä määrä viestejä per keskusteluketju

V 0.5
   - lisätty salainen huone, joka näkyy vain määritetyille käyttäjille
   - admin pystyy lisäämään / poistamaan käyttäjiä huoneesta
   - huone näkyy index-sivulla vain sen jäsenille

V 0.5.1
   - korjattu salaisen huoneen bugi, jossa kuka tahansa käyttäjä pystyi lisäämään / poistamaan jäseniä
   - korjattu bugi, jossa keskusteluketju ja viestiketju eivät toimineet, mikäli viestin määrä on 0

v 0.5.2
   - korjattu bugi, jossa keskusteluketjun otsikkoa ei pystynyt muokkaamaan / poistamaan, mikäli viestien määrä oli 0