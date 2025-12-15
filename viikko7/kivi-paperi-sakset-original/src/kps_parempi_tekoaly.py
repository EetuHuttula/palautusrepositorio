from tekoaly_parannettu import TekoalyParannettu
from kps_pelaaja_template import KPSPelaajaTemplate


class KPSParempiTekoaly(KPSPelaajaTemplate):
    def _alusta(self):
        self._tekoaly = TekoalyParannettu(10)

    def _toinen_siirto(self, ekan_siirto):
        return self._tekoaly.anna_siirto()

    def _ilmoita_tok_siirto(self, siirto):
        print(f"Tietokone valitsi: {siirto}")

    def _aseta_siirto(self, siirto):
        self._tekoaly.aseta_siirto(siirto)

