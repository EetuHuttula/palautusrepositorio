import pytest
from tuomari import Tuomari


class TestTuomari:
    """Testit Tuomari-luokalle"""
    
    def setup_method(self):
        """Alustetaan tuomari ennen jokaista testiä"""
        self.tuomari = Tuomari()
    
    def test_alustus(self):
        """Testaa että tuomari alustetaan oikein"""
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0
    
    def test_tasapeli_kivi_kivi(self):
        """Testaa tasapeli kun molemmat valitsevat kiven"""
        self.tuomari.kirjaa_siirto("k", "k")
        assert self.tuomari.tasapelit == 1
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0
    
    def test_tasapeli_paperi_paperi(self):
        """Testaa tasapeli kun molemmat valitsevat paperin"""
        self.tuomari.kirjaa_siirto("p", "p")
        assert self.tuomari.tasapelit == 1
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0
    
    def test_tasapeli_sakset_sakset(self):
        """Testaa tasapeli kun molemmat valitsevat sakset"""
        self.tuomari.kirjaa_siirto("s", "s")
        assert self.tuomari.tasapelit == 1
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0
    
    def test_eka_voittaa_kivi_sakset(self):
        """Testaa että kivi voittaa sakset"""
        self.tuomari.kirjaa_siirto("k", "s")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0
    
    def test_eka_voittaa_paperi_kivi(self):
        """Testaa että paperi voittaa kiven"""
        self.tuomari.kirjaa_siirto("p", "k")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0
    
    def test_eka_voittaa_sakset_paperi(self):
        """Testaa että sakset voittaa paperin"""
        self.tuomari.kirjaa_siirto("s", "p")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0
    
    def test_toka_voittaa_kivi_paperi(self):
        """Testaa että paperi voittaa kiven"""
        self.tuomari.kirjaa_siirto("k", "p")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0
    
    def test_toka_voittaa_paperi_sakset(self):
        """Testaa että sakset voittaa paperin"""
        self.tuomari.kirjaa_siirto("p", "s")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0
    
    def test_toka_voittaa_sakset_kivi(self):
        """Testaa että kivi voittaa sakset"""
        self.tuomari.kirjaa_siirto("s", "k")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0
    
    def test_usean_kierroksen_pisteet(self):
        """Testaa pisteiden laskeminen usealla kierroksella"""
        self.tuomari.kirjaa_siirto("k", "s")  # eka voittaa
        self.tuomari.kirjaa_siirto("p", "p")  # tasapeli
        self.tuomari.kirjaa_siirto("s", "k")  # toka voittaa
        self.tuomari.kirjaa_siirto("k", "s")  # eka voittaa
        
        assert self.tuomari.ekan_pisteet == 2
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 1
    
    def test_str_metodi(self):
        """Testaa tuomarin merkkijonoesitys"""
        self.tuomari.kirjaa_siirto("k", "s")
        self.tuomari.kirjaa_siirto("p", "p")
        
        tulos = str(self.tuomari)
        assert "1 - 0" in tulos
        assert "Tasapelit: 1" in tulos
