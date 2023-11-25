# Keskustelusovellus

Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Sovelluksen ominaisuuksia:

   - Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
   - Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
   - Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
   - Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
   - Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
   - Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
   - Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
   - Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

Testaus:
   - kopioi repositorio
   - luo .env tiedosto, sinne tulee luoda SECRET_KEY esim. komennolla python3, import secrets, secret.token_hex(16)
   - luo tietokanta käyttäen sql-skeemaa
   - aja pip install -r requirements.txt
   - venv-ympäristö käyttöön komennolla source/bin/activate
   - testiympäristö käyttöön komennolla flask run
   - sql-kantaan tulee luoda kolme aihetta topic-tauluun, "general", "politics" ja "economy"
   - sovellus alkaa toimia järkevämmin, kun luo ensimmäisen keskusteluketjun jokaisen aiheen alle

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
