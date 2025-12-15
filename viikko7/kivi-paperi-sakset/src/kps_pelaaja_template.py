from tuomari import Tuomari


class KPSPelaajaTemplate:
    def pelaa(self):
        tuomari = Tuomari()
        self._alusta()

        ekan_siirto = self._ensimmainen_siirto()
        tokan_siirto = self._toinen_siirto(ekan_siirto)
        self._ilmoita_tok_siirto(tokan_siirto)

        while self._onko_ok_siirto(ekan_siirto) and self._onko_ok_siirto(tokan_siirto):
            tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(tuomari)

            ekan_siirto = self._ensimmainen_siirto()
            tokan_siirto = self._toinen_siirto(ekan_siirto)
            self._ilmoita_tok_siirto(tokan_siirto)
            self._aseta_siirto(ekan_siirto)

        print("Kiitos!")
        print(tuomari)

    def _alusta(self):
        """Alustaa pelin — ei oletuksena tee mitään."""
        pass

    def _ensimmainen_siirto(self):
        return input("Ensimmäisen pelaajan siirto: ")

    def _toinen_siirto(self, ekan_siirto):
        """Palauttaa toisen pelaajan siirron. Pakollinen ylikirjoitus.
        """
        raise NotImplementedError()

    def _ilmoita_tok_siirto(self, siirto):
        """Valinnainen: ilmoittaa toisen pelaajan (esim. tekoälyn) valinnan."""
        pass

    def _aseta_siirto(self, siirto):
        """Valinnainen: annetaan tekoälylle tieto ekan siirrosta."""
        pass

    def _onko_ok_siirto(self, siirto):
        return siirto == "k" or siirto == "p" or siirto == "s"
