import pytest
from tekoaly import Tekoaly


class TestTekoaly:
    """Testit yksinkertaiselle tekoälylle"""
    
    def setup_method(self):
        """Alustetaan tekoäly ennen jokaista testiä"""
        self.tekoaly = Tekoaly()
    
    def test_alustus(self):
        """Testaa että tekoäly alustetaan oikein"""
        assert self.tekoaly._siirto == 0
    
    def test_ensimmainen_siirto_on_kivi(self):
        """Testaa että ensimmäinen siirto on paperi (laskuri alkaa 0:sta, kasvatetaan 1:ksi)"""
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "p"
    
    def test_toinen_siirto_on_paperi(self):
        """Testaa että toinen siirto on sakset"""
        self.tekoaly.anna_siirto()  # ensimmäinen
        siirto = self.tekoaly.anna_siirto()  # toinen
        assert siirto == "s"
    
    def test_kolmas_siirto_on_sakset(self):
        """Testaa että kolmas siirto on kivi"""
        self.tekoaly.anna_siirto()  # ensimmäinen
        self.tekoaly.anna_siirto()  # toinen
        siirto = self.tekoaly.anna_siirto()  # kolmas
        assert siirto == "k"
    
    def test_siirrot_toistuvat_syklissa(self):
        """Testaa että siirrot toistuvat kolmen siirron syklissä"""
        odotetut = ["p", "s", "k", "p", "s", "k", "p", "s", "k"]
        
        for odotettu in odotetut:
            assert self.tekoaly.anna_siirto() == odotettu
    
    def test_aseta_siirto_ei_tee_mitaan(self):
        """Testaa että aseta_siirto ei vaikuta yksinkertaiseen tekoälyyn"""
        self.tekoaly.aseta_siirto("k")
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "p"  # Pitäisi olla ensimmäinen siirto
