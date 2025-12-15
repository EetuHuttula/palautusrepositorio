from tuomari import Tuomari
from tekoaly import Tekoaly
from kps_pelaaja_template import KPSPelaajaTemplate


class KPSTekoaly(KPSPelaajaTemplate):
    def _alusta(self):
        self._tekoaly = Tekoaly()

    def _toinen_siirto(self, ekan_siirto):
        return self._tekoaly.anna_siirto()

    def _ilmoita_tok_siirto(self, siirto):
        print(f"Tietokone valitsi: {siirto}")

