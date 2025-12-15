from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


def luo_peli(valinta):
    if valinta is None:
        return None

    if valinta.endswith("a"):
        return KPSPelaajaVsPelaaja()
    if valinta.endswith("b"):
        return KPSTekoaly()
    if valinta.endswith("c"):
        return KPSParempiTekoaly()

    return None
