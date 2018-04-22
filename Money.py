from collections import Counter

class Money():
    def __init__(self):
        self._ilosc = {'1': 0, '2': 0, '5': 0, '10': 0, '20': 0, '50': 0, '100': 0, '200': 0, '500': 0,
                       '1000': 0, '2000': 0, '5000': 0, '10000': 0, '20000': 0}
        #self._ilosc = {str(x*10**y) : 0 for x in [1,2,5] for y in range(5)}
        self._wartosc = 0

    def dodaj(self, n1, n2, n5, n10, n20, n50, n100, n200, n500, n1000, n2000, n5000, n10000, n20000):
        lista = [0] * 14
        lista = [n1, n2, n5, n10, n20, n50, n100, n200, n500, n1000, n2000, n5000, n10000, n20000]
        self.dodaj_liste(lista)

    def dodaj_liste(self, lista):
        self._ilosc['1'] = lista[0]
        self._ilosc['2'] = lista[1]
        self._ilosc['5'] = lista[2]
        self._ilosc['10'] = lista[3]
        self._ilosc['20'] = lista[4]
        self._ilosc['50'] = lista[5]
        self._ilosc['100'] = lista[6]
        self._ilosc['200'] = lista[7]
        self._ilosc['500'] = lista[8]
        self._ilosc['1000'] = lista[9]
        self._ilosc['2000'] = lista[10]
        self._ilosc['5000'] = lista[11]
        self._ilosc['10000'] = lista[12]
        self._ilosc['20000'] = lista[13]

    def wypisz(self):
        for x in self._ilosc.values():
            print(x, end=' ')

    def doString(self):
        tekst = ""
        for x in self._ilosc.items():
            tekst += str(int(x[0])/100)
            tekst += " zł\tx "
            tekst += str(int(x[1]))
            tekst += "\n"
        return tekst


    def wartosci(self):
        for x in self._ilosc.items():
            print(int(x[0])*x[1], end = ' ')

    def oblicz_wartosc(self):
        suma = 0
        for x in self._ilosc.items():
            suma += int(x[0])*x[1]
        self._wartosc = suma
        return suma

    @staticmethod #decorator
    def suma(a, b):

        aa = a.zwroc_slownik()
        bb = b.zwroc_slownik()

        zbior1 = list(aa.values())
        zbior2 = list(bb.values())

        for x in range (14):
            zbior1[x] += zbior2[x]

        suma = Money()

        suma.dodaj_liste(zbior1)
        return suma

    @staticmethod #decorator
    def roznica(a, b):

        aa = a.zwroc_slownik()
        bb = b.zwroc_slownik()

        zbior1 = list(aa.values())
        zbior2 = list(bb.values())

        for x in range (14):
            zbior1[x] -= zbior2[x]

        suma = Money()

        suma.dodaj_liste(zbior1)
        return suma

    def wydaj(self, kwota_do_wydania):

        nominal = list(self._ilosc.keys()) #str
        ilosc = list(self._ilosc.values())

        nominal.reverse()
        ilosc.reverse()
        ilosc_reszta = [0] * 14
        for i in range(14):
            while (not ((int(nominal[i])) > kwota_do_wydania) and ilosc[i] > 0):
                kwota_do_wydania -= int(nominal[i])
                ilosc[i] -= 1
                ilosc_reszta[i] += 1

        nominal.reverse()
        ilosc.reverse()
        ilosc_reszta.reverse()

        zostalo = dict(zip(nominal, ilosc))
        reszta = dict(zip(nominal, ilosc_reszta))

        if kwota_do_wydania == 0:
            return (zostalo, reszta)
        else:
            return -1  # nie da się wydać

    def zwroc_wartosc(self):
        tab = list(self._ilosc.values())
        return tab

    def zwroc_klucze(self):
        tab = list(self._ilosc.keys())
        return tab

    def zwroc_slownik(self):
        return self._ilosc


