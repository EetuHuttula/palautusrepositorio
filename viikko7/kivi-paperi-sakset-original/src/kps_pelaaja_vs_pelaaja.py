from tuomari import Tuomari
from kps_pelaaja_template import KPSPelaajaTemplate


class KPSPelaajaVsPelaaja(KPSPelaajaTemplate):
    def _toinen_siirto(self, ekan_siirto):
        return input("Toisen pelaajan siirto: ")

