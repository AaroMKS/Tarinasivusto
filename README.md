# Tarinasivusto
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tarinoita.
* Käyttäjä pystyy lisäämään kuvia lisäksi tarinoihin.
* Käyttäjä näkee sovellukseen lisätyt tarinat.
* Käyttäjä pystyy etsimään tarinoita hakusanalla.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät tarinat.
* Käyttäjä pystyy valitsemaan tarinalle yhden tai useamman luokittelun (esim. genre, pituus, ikärajaluokitus).
* Käyttäjä pystyy arvioimaan julkaistuja tarinoita.

Sovelluksen nykyinen tilanne:
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tarinoita.
* Käyttäjä näkee sovellukseen lisätyt tarinat.
* Käyttäjä pystyy etsimään tarinoita hakusanalla.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän lisäämät tarinat.
* Käyttäjä pystyy valitsemaan tarinalle luokitteluksi genren ja ikärajaluokituksen
* Käyttäjä pystyy arvioimaan julkaistuja tarinoita.
  
##Sovelluksen käynnistys
Asenna "flask"-kirjasto:
```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Käynnistä sovellus:
```
$flask run
```
