# Testit - Kivi-Paperi-Sakset

Tämä projekti sisältää kattavat testit sekä pelilogiikalle että web-sovellukselle.

## Testikohteet

### 1. Pelilogiikan testit

#### `test_tuomari.py` - Tuomari-luokka (12 testiä)
- ✅ Alustus
- ✅ Tasapelitilanteet (kivi-kivi, paperi-paperi, sakset-sakset)
- ✅ Pelaaja 1 voittotilanteet (kivi-sakset, paperi-kivi, sakset-paperi)
- ✅ Pelaaja 2 voittotilanteet (kivi-paperi, paperi-sakset, sakset-kivi)
- ✅ Usean kierroksen pisteiden seuranta
- ✅ Merkkijonoesitys

#### `test_tekoaly.py` - Yksinkertainen tekoäly (6 testiä)
- ✅ Alustus
- ✅ Siirtojen sykli (paperi → sakset → kivi → paperi...)
- ✅ Siirtojen toistuminen
- ✅ aseta_siirto ei vaikuta toimintaan

#### `test_tekoaly_parannettu.py` - Parannettu tekoäly (9 testiä)
- ✅ Alustus ja muistin koko
- ✅ Ensimmäiset siirrot ilman historiaa
- ✅ Muistin päivitys
- ✅ Muistin täyttyminen ja kierto
- ✅ Ennustukset pelaajan siirtojen perusteella
- ✅ Siirtojen laskenta muistista

#### `test_kps_tehdas.py` - Pelitehdas (8 testiä)
- ✅ Pelaaja vs Pelaaja -pelin luonti
- ✅ Pelaaja vs Tekoäly -pelin luonti
- ✅ Pelaaja vs Parannettu Tekoäly -pelin luonti
- ✅ Virheellisten valintojen käsittely
- ✅ None-arvojen käsittely

### 2. Web-sovelluksen testit

#### `test_web_app.py` - Flask-sovellus (17 testiä)
- ✅ Pääsivun latautuminen
- ✅ Pelitilavalinnat
- ✅ Pelien aloitus (PvP, vs AI, vs Advanced AI)
- ✅ Navigointi ilman aktiivista peliä
- ✅ Siirrot PvP-tilassa (tasapeli, voitot)
- ✅ Siirrot tekoälyä vastaan
- ✅ Siirrot parannettua tekoälyä vastaan
- ✅ Virheellisten siirtojen käsittely
- ✅ Reset-toiminnallisuus
- ✅ Pisteiden seuranta usealla kierroksella
- ✅ Tekoälyn tilan päivittyminen
- ✅ Parannetun tekoälyn muistin päivittyminen
- ✅ Pelihistorian tallentuminen

## Testien ajaminen

### Kaikki testit
```bash
cd src
pytest tests/ -v
```

### Yksittäinen testitiedosto
```bash
pytest tests/test_tuomari.py -v
pytest tests/test_web_app.py -v
```

### Testit coverage-raportin kanssa
```bash
pytest tests/ --cov=. --cov-report=term-missing --cov-report=html
```

Coverage-raportti luodaan `htmlcov/`-hakemistoon. Avaa `htmlcov/index.html` selaimessa.

### Nopea testien ajo ilman outputtia
```bash
pytest tests/ -q
```

## Testikattavuus

**Kokonaiskattavuus: 90%**

| Moduuli | Kattavuus | Huomiot |
|---------|-----------|---------|
| `tuomari.py` | 100% | Täysi kattavuus |
| `tekoaly.py` | 100% | Täysi kattavuus |
| `tekoaly_parannettu.py` | 100% | Täysi kattavuus |
| `kps_tehdas.py` | 100% | Täysi kattavuus |
| `web_app.py` | 79% | Web-sovelluksen ydinlogiikka testattu |
| `kps_pelaaja_template.py` | 31% | Template-luokka, ei suoraan testattava |
| `kps_tekoaly.py` | 70% | Päälogiikka testattu |
| `kps_parempi_tekoaly.py` | 64% | Päälogiikka testattu |
| `index.py` | 0% | CLI-sovellus, ei web-testeissä |

## Riippuvuudet

Testit vaativat seuraavat paketit (asennettu automaattisesti):
- `pytest` - Testauskehys
- `pytest-flask` - Flask-sovellusten testaus
- `pytest-cov` - Kattavuusraportointi
- `coverage` - Koodin kattavuuden mittaus

## Continuous Integration

Testit voidaan ajaa osana CI/CD-putkea. Esimerkki GitHub Actions -konfiguraatiosta:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-flask pytest-cov
      - name: Run tests
        run: |
          cd src
          pytest tests/ --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Testin kehittäminen

Kun lisäät uusia ominaisuuksia:

1. **Kirjoita testi ensin** (TDD - Test-Driven Development)
2. **Varmista että testi epäonnistuu** aluksi
3. **Toteuta ominaisuus** niin että testi menee läpi
4. **Refaktoroi** tarvittaessa
5. **Varmista että kaikki testit menevät läpi**

### Esimerkki uuden testin lisäämisestä:

```python
def test_uusi_ominaisuus(self, client):
    """Testaa uutta ominaisuutta"""
    # Arrange - valmistele
    with client.session_transaction() as session:
        session['game_mode'] = 'a'
    
    # Act - suorita
    response = client.post('/uusi-endpoint', data={'key': 'value'})
    
    # Assert - tarkista
    assert response.status_code == 200
    assert b'expected_content' in response.data
```

## Testien rakenne

Testit noudattavat AAA-mallia (Arrange-Act-Assert):
- **Arrange**: Valmistele testidata ja ympäristö
- **Act**: Suorita testattava toiminto
- **Assert**: Varmista että tulos on odotettu

## Ongelmatilanteissa

Jos testit epäonnistuvat:

1. Tarkista virheviestit huolellisesti
2. Aja yksittäinen testi: `pytest tests/test_file.py::TestClass::test_method -v`
3. Käytä debuggeria: `pytest tests/test_file.py --pdb`
4. Tarkista että kaikki riippuvuudet on asennettu
5. Varmista että olet oikeassa hakemistossa (`src/`)

## Yhteenveto

✅ **52 testiä yhteensä**
✅ **Kaikki testit menevät läpi**
✅ **90% koodin kattavuus**
✅ **Testit kattavat sekä yksikkö- että integraatiotestauksen**
