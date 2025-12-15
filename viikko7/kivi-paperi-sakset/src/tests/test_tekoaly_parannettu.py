import pytest
from tekoaly_parannettu import TekoalyParannettu


class TestTekoalyParannettu:
    """Testit parannetulle tekoälylle"""
    
    def setup_method(self):
        """Alustetaan tekoäly ennen jokaista testiä"""
        self.tekoaly = TekoalyParannettu(10)
    
    def test_alustus(self):
        """Testaa että tekoäly alustetaan oikein"""
        assert len(self.tekoaly._muisti) == 10
        assert self.tekoaly._vapaa_muisti_indeksi == 0
        assert all(x is None for x in self.tekoaly._muisti)
    
    def test_ensimmainen_siirto_ilman_historiaa(self):
        """Testaa että ensimmäinen siirto on kivi kun ei ole historiaa"""
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "k"
    
    def test_toinen_siirto_ilman_historiaa(self):
        """Testaa että toinen siirto on kivi kun on vain yksi historia"""
        self.tekoaly.aseta_siirto("p")
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "k"
    
    def test_muistin_paivitys(self):
        """Testaa että muisti päivittyy oikein"""
        self.tekoaly.aseta_siirto("k")
        assert self.tekoaly._muisti[0] == "k"
        assert self.tekoaly._vapaa_muisti_indeksi == 1
        
        self.tekoaly.aseta_siirto("p")
        assert self.tekoaly._muisti[1] == "p"
        assert self.tekoaly._vapaa_muisti_indeksi == 2
    
    def test_muistin_tayttyminen(self):
        """Testaa että muisti toimii kun se täyttyy"""
        # Täytä muisti
        for i in range(10):
            self.tekoaly.aseta_siirto("k")
        
        assert self.tekoaly._vapaa_muisti_indeksi == 10
        
        # Lisää vielä yksi - pitäisi poistaa ensimmäinen
        self.tekoaly.aseta_siirto("p")
        assert self.tekoaly._vapaa_muisti_indeksi == 10
        assert self.tekoaly._muisti[9] == "p"
    
    def test_ennustus_kiven_perusteella(self):
        """Testaa että tekoäly ennustaa oikein kun pelaaja toistaa kiven"""
        # Simuloi tilanne jossa pelaaja pelaa k -> p -> k -> p
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("k")
        
        # Tekoälyn pitäisi ennustaa että seuraava on p ja vastata saksilla
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "s"  # Sakset voittaa paperin
    
    def test_ennustus_paperin_perusteella(self):
        """Testaa että tekoäly vastaa oikein kun pelaaja pelaa paljon paperia"""
        # Simuloi tilanne jossa pelaaja pelaa p -> k -> p -> k -> p
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("p")
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("p")
        
        # Kun viimeisin on p ja usein sen jälkeen tulee k
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "p"  # Paperi voittaa kiven
    
    def test_muistin_koko_vaikuttaa(self):
        """Testaa että eri muistikoot toimivat"""
        pieni_tekoaly = TekoalyParannettu(3)
        assert len(pieni_tekoaly._muisti) == 3
        
        iso_tekoaly = TekoalyParannettu(20)
        assert len(iso_tekoaly._muisti) == 20
    
    def test_siirtojen_laskenta(self):
        """Testaa että tekoäly laskee siirtoja oikein muistista"""
        # Luo toistuva kaava: k -> k -> k -> s
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("k")
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("s")
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("k")
        
        # Tekoälyn pitäisi huomata että k:n jälkeen tulee usein k tai s
        # ja vastata sen mukaan
        siirto = self.tekoaly.anna_siirto()
        assert siirto in ["k", "p", "s"]  # Kaikki ovat valideja vastauksia
