import Money as m

class TicketMachine():
    def __init__(self):
        self._stan = m.Money()
        #self._stan.dodaj(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) # sytuacja gdzie automat ma tylko jeden grosz
        self._stan.dodaj(10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10)

        self._wplacone = m.Money()
        self._wplacone.dodaj(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self._suma = m.Money() #stan automatu + wplaconych pieniędzy
        self._suma = m.Money.suma(self._stan, self._wplacone)

    def wplata(self, n1, n2, n5, n10, n20, n50, n100, n200, n500, n1000, n2000, n5000, n10000, n20000):
        self._wplacone.dodaj(n1, n2, n5, n10, n20, n50, n100, n200, n500, n1000, n2000, n5000, n10000, n20000)

    def wplataP(self, money):
        self._wplacone.dodaj_liste(money)

    def zwroc_slownik(self, i):
        if i == 1:
            return dict(zip(self._stan.zwroc_klucze(), self._stan.zwroc_wartosc()))
        elif i == 2:
            return dict(zip(self._stan.zwroc_klucze(), self._wplacone.zwroc_wartosc()))
        else:
            return dict(zip(self._stan.zwroc_klucze(), self._suma.zwroc_wartosc()))

    def zwroc_wartosci(self, i):
        if i == 1:
            return self._stan.zwroc_wartosc()
        elif i == 2:
            return self._wplacone.zwroc_wartosc()
        else:
            return self._suma.zwroc_wartosc()


    def pokaz_stan(self, i):
        if i == 1:
            return self._stan.oblicz_wartosc()
        elif i == 2:
            return self._wplacone.oblicz_wartosc()
        else:
            return self._suma.oblicz_wartosc()

    def zmiana(self):
        self._suma = m.Money.suma(self._stan, self._wplacone)

    def zwroc_stan(self, i):

        if i == 1:
            tytul = "Aktualny stan automatu: "
            zmienna = self._suma
        else:
            tytul = "Wpłacone pieniądze: "
            zmienna = self._wplacone

        tekst = ""
        tekst += tytul
        tekst += str(zmienna.oblicz_wartosc()/100)
        tekst += " zł\n"
        tekst += zmienna.doString()
        return tekst

    def zwrot(self):
        self._suma = m.Money.roznica(self._suma, self._wplacone)
        lista = [0] * 14
        self._wplacone.dodaj_liste(lista)

    def oblicz_reszte(self, kwota_zakupu):
        print("\n")
        if (self._wplacone.oblicz_wartosc() > kwota_zakupu):

            #Ile automat ma wydać
            do_wydania = self._wplacone.oblicz_wartosc() - kwota_zakupu

            #Czy automat jest w stanie tyle wydać?
            if (self._suma.wydaj(do_wydania)) != -1:

                krotka = self._suma.wydaj(do_wydania)

                tab = list(krotka[0].values())
                self._stan.dodaj_liste(tab)
                self._suma.dodaj_liste(tab)
                self._wplacone.dodaj_liste([0] * 14)

                return krotka[1]

            else:
                print("Nie da się wydać")
                self._suma = m.Money.roznica(self._suma, self._wplacone)
                # po returnie czyszcze liste _wplacone
                return "Nie ma jak wydać"

        elif (self._wplacone.oblicz_wartosc() == kwota_zakupu):
            self._stan = m.Money.suma(self._stan, self._wplacone) #aktualizacja stanu maszyny
            self._wplacone.dodaj_liste([0]*14)
            return "zakup bez reszty"
        else:
            return "za mała wpłata"





