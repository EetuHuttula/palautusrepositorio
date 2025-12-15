import pytest
from kps_tehdas import luo_peli
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


class TestKpsTehdas:
    """Testit pelitehtaalle"""
    
    def test_luo_pelaaja_vs_pelaaja(self):
        """Testaa että 'a' luo pelaaja vs pelaaja -pelin"""
        peli = luo_peli("a")
        assert isinstance(peli, KPSPelaajaVsPelaaja)
    
    def test_luo_pelaaja_vs_pelaaja_paattyy_a(self):
        """Testaa että mikä tahansa 'a':lla päättyvä merkkijono luo PvP-pelin"""
        peli = luo_peli("aa")
        assert isinstance(peli, KPSPelaajaVsPelaaja)
        
        peli = luo_peli("xa")
        assert isinstance(peli, KPSPelaajaVsPelaaja)
    
    def test_luo_tekoaly_peli(self):
        """Testaa että 'b' luo tekoälypelin"""
        peli = luo_peli("b")
        assert isinstance(peli, KPSTekoaly)
    
    def test_luo_tekoaly_peli_paattyy_b(self):
        """Testaa että mikä tahansa 'b':llä päättyvä merkkijono luo tekoälypelin"""
        peli = luo_peli("bb")
        assert isinstance(peli, KPSTekoaly)
        
        peli = luo_peli("xb")
        assert isinstance(peli, KPSTekoaly)
    
    def test_luo_parannettu_tekoaly_peli(self):
        """Testaa että 'c' luo parannetun tekoälypelin"""
        peli = luo_peli("c")
        assert isinstance(peli, KPSParempiTekoaly)
    
    def test_luo_parannettu_tekoaly_peli_paattyy_c(self):
        """Testaa että mikä tahansa 'c':llä päättyvä merkkijono luo parannetun tekoälypelin"""
        peli = luo_peli("cc")
        assert isinstance(peli, KPSParempiTekoaly)
        
        peli = luo_peli("xc")
        assert isinstance(peli, KPSParempiTekoaly)
    
    def test_virheellinen_valinta_palauttaa_none(self):
        """Testaa että virheellinen valinta palauttaa None"""
        peli = luo_peli("d")
        assert peli is None
        
        peli = luo_peli("x")
        assert peli is None
        
        peli = luo_peli("")
        assert peli is None
    
    def test_none_palauttaa_none(self):
        """Testaa että None-arvo palauttaa None"""
        peli = luo_peli(None)
        assert peli is None
