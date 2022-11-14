import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_kassapaatteen_rahamaara_ja_myytyjen_lounaiden_maara_oikea(self):
        rahaa = self.kassapaate.kassassa_rahaa
        edulliset = self.kassapaate.edulliset
        maukkaat = self.kassapaate.maukkaat

        self.assertEqual(rahaa, 100000)
        self.assertEqual(edulliset, 0)
        self.assertEqual(maukkaat, 0)
        
    def test_edullinen_lounas_kasvattaa_rahamaaraa_ja_antaa_oikean_vaihtorahan(self):
        vaihtorahaa = self.kassapaate.syo_edullisesti_kateisella(300)
        rahaa = self.kassapaate.kassassa_rahaa

        self.assertEqual(rahaa, 100240)
        self.assertEqual(vaihtorahaa, 60)

    def test_myytyjen_edullisten_lounaiden_maara_kasvaa_kateisella(self):
        self.kassapaate.syo_edullisesti_kateisella(300)

        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukas_lounas_kasvattaa_rahamaaraa_ja_antaa_oikean_vaihtorahan(self):
        vaihtorahaa = self.kassapaate.syo_maukkaasti_kateisella(500)
        rahaa = self.kassapaate.kassassa_rahaa

        self.assertEqual(rahaa, 100400)
        self.assertEqual(vaihtorahaa, 100)

    def test_myytyjen_maukkaiden_lounaiden_maara_kasvaa_kateisella(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassapaate.maukkaat, 1)
        
    def test_maksu_ei_riittava_edullisesti_kassan_rahamaara_ei_muutu(self):
        vaihtorahaa = self.kassapaate.syo_edullisesti_kateisella(200)
        rahaa = self.kassapaate.kassassa_rahaa

        self.assertEqual(rahaa, 100000)
        self.assertEqual(vaihtorahaa, 200)
    
    def test_kateismaksu_ei_riittava_edullisten_lounaiden_maara_sama(self):
        self.kassapaate.syo_edullisesti_kateisella(200)

        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maksu_ei_riittava_maukkaasti_kassan_rahamaara_ei_muutu(self):
        vaihtorahaa = self.kassapaate.syo_maukkaasti_kateisella(200)
        rahaa = self.kassapaate.kassassa_rahaa

        self.assertEqual(rahaa, 100000)
        self.assertEqual(vaihtorahaa, 200)
    
    def test_kateismaksu_ei_riittava_maukkaiden_lounaiden_maara_sama(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)

        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_jos_kortilla_tarpeeksi_rahaa_veloitetaan_summa_palautetaan_true_edullinen(self):
        palaute = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)

        self.assertEqual(palaute, True)

    def test_jos_kortilla_tarpeeksi_rahaa_veloitetaan_summa_palautetaan_true_maukas(self):
        palaute = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)

        self.assertEqual(palaute, True)

    def test_kortilla_tarpeeksi_rahaa_myytyjen_edullisten_maara_kasvaa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti) 

        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kortilla_tarpeeksi_rahaa_myytyjen_maukkaiden_maara_kasvaa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti) 

        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kortilla_ei_tarpeeksi_rahaa_kortin_raha_ei_muutu_palautetaan_false_ed(self):
        kortti = Maksukortti(100)
        palaute = self.kassapaate.syo_edullisesti_kortilla(kortti)

        self.assertEqual(str(kortti), "Kortilla on rahaa 1.00 euroa")
        self.assertEqual(palaute, False)

    def test_kortilla_ei_tarpeeksi_rahaa_kortin_raha_ei_muutu_palautetaan_false_mau(self):
        kortti = Maksukortti(100)
        palaute = self.kassapaate.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(str(kortti), "Kortilla on rahaa 1.00 euroa")
        self.assertEqual(palaute, False)

    def test_kortilla_ei_tarpeeksi_rahaa_myytyjen_lounaiden_maara_ei_muutu(self):
        kortti = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kassan_rahamaara_ei_muutu_jos_raha_ei_riita(self):
        kortti = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(kortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kortin_saldo_muuttuu_rahaa_ladattaessa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)

        self.assertEqual(self.maksukortti.saldo, 1100)

    def test_kassan_rahamaara_kasvaa_ladattaessa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100100)

    def test_kassan_rahamaara_ei_muutu_negatiivisen_summan_ladattaessa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -100)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
