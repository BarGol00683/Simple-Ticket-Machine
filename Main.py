from appJar import gui
import TicketMachine as tick
from Ticket import Ticket

ticketmachine = tick.TicketMachine()

item = [None for _ in range(6)]
item[0] = Ticket("2 zł", 200, "20U")
item[1] = Ticket("2.40 zł", 240, "20N")
item[2] = Ticket("1.80 zł", 180, "40U")
item[3] = Ticket("3.40 zł", 340, "40N")
item[4] = Ticket("2.50 zł", 250, "60U")
item[5] = Ticket("5.00 zł", 500, "60N")

def update():

    zlotowki = lambda x: (x / 100)

    w_automacie = str(zlotowki(ticketmachine.pokaz_stan(2))) + " zł"
    app.setLabel("wplacone", w_automacie)
    wplacone2 = ((zlotowki(ticketmachine.pokaz_stan(3))*100) - (zlotowki(ticketmachine.pokaz_stan(1)))*100) / 100
    wplacone3 = round(wplacone2, 2)
    stan = "Pieniędzy w automacie " + str(zlotowki(ticketmachine.pokaz_stan(1))) + " zł + ( " + str(wplacone2) + " zł )"  \
           + "\n" + "Wplacone pieniądze: " +str(wplacone2) + " zł"
    app.setLabel("automat_stan", stan)

def update_label():
    tekst = ticketmachine.zwroc_stan(1)
    app.setLabel("Stan automatu", tekst)
    tekst = ticketmachine.zwroc_stan(2)
    app.setLabel("wrzucone_pinionszki", tekst)

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def HowMuch(item): #ILOSC
    tekst = "Proszę podać ilość biletów\n" + item.returnName() + "\n"
    ilosc = app.textBox("Podaj ilość", tekst)
    if ilosc is None:
        ilosc = 0

    if ((RepresentsInt(ilosc)) and (int(ilosc) >= 0)):
        for i in range(int(ilosc)):
            app.addListItem("koszyk", item.returnName())
    else:
        app.warningBox("Błąd", "Proszę podać właściwą ilość")
    ilosc2 = (int(ilosc)) + (int(app.getLabel("suma")))
    app.setLabel("suma", (str(ilosc2)))

def Check1(i):
    if (int(i)) == 0:
        zakupy = app.getListItems("koszyk")
    elif (int(i)) == 1:
        zakupy = app.getAllListItems("koszyk")
    cenka = 0
    cenka2 = 0

    if not zakupy:
        app.warningBox("Błąd", "Proszę wybrać bilety z listy obok")
    else:
        for k in range(6):
            for a in zakupy:
                if a == item[k].returnName():
                    cenka += item[k].returnPrice()
    cenka2 = cenka / 100
    app.setLabel("do_zapl", (str(cenka2)) + " zł")
    app.setLabel("do_zapl2", (str(cenka2)) + " zł")

def Check2(i):
    if (int(i)) == 0:
        zakupy = app.getListItems("koszyk")
    elif (int(i)) == 1:
        zakupy = app.getAllListItems("koszyk")
    cenka = 0
    cenka2 = 0

    if not zakupy:
        app.warningBox("Błąd", "Proszę wybrać bilety z listy obok")
    else:
        if ticketmachine.pokaz_stan(2) != 0:
            tekst = "Czy napewno chcesz kupić: \n\n"

            licznik = [0] * 6
            do_zaplaty = [0] * 6
            suma = 0

            for k in range(6):
                for a in zakupy:
                    if a == item[k].returnName():
                        licznik[k] += 1
                        do_zaplaty[k] += item[k].returnPrice()
                        cenka += item[k].returnPrice()

            cenka2 = cenka / 100
            app.setLabel("do_zapl", (str(cenka2)) + " zł")
            app.setLabel("do_zapl2", (str(cenka2)) + " zł")

            for k in range(6):
                suma += do_zaplaty[k]
                tekst += item[k].returnName()
                tekst += "\t "
                tekst += str(licznik[k])
                tekst += " x "
                tekst += str(item[k].returnPrice() / 100)
                tekst += "\t= "
                tekst += str(do_zaplaty[k] / 100)
                tekst += " zł"
                tekst += "\n"
            tekst += "-" * 50
            tekst += "\nrazem do zapłaty:\t "
            tekst += str(suma / 100)
            tekst += " zł"

            if (app.yesNoBox("Zakup", tekst)) == True:
                wynik = ticketmachine.oblicz_reszte(suma)

                if wynik == "nie ma jak wydac":
                    tekst = "Niestety automat nie ma jak wydać,\n automat zwraca to co dostał\n\n" + str(
                        ticketmachine.zwroc_stan(2))
                    app.warningBox("Błąd", tekst)

                    ticketmachine.wplataP([0] * 14)
                    update()
                elif wynik == "zakup bez reszty":
                    app.infoBox("Potwierdzenie", "Dziękujemy za zakup biletów, bez reszty\n")
                    update()
                elif wynik == "za mała wpłata":
                    app.warningBox("Błąd", "Za mało pieniędzy")
                else:
                    tekst = "Dziękujemy za zakup biletów\n Twoja reszta:\n"

                    for x in wynik.items():
                        tekst += str(int(x[0]) / 100)
                        tekst += " zł\tx "
                        tekst += str(int(x[1]))
                        tekst += "\n"

                    app.infoBox("Potwierdzenie", tekst)
                    update()
            else:
                pass
        else:
            app.warningBox("Błąd", "Wrzuć Monety")
    update_label()


def press(btn): # PRZYCISKI

    tekst = ticketmachine.zwroc_stan(2)
    app.setLabel("wrzucone_pinionszki", tekst)

    for i in range(6):
        if btn == item[i].returnName():
            HowMuch(item[i])

    if btn == "Cena wybranych biletów":
        Check1(0)

    if btn == "Cena wszystkich biletów":
        Check1(1)

    if btn == "Usuń wybrany bilet":
        items = app.getListItems("koszyk")
        if len(items) > 0:
            app.removeListItem("koszyk", items[0])
        if (int(app.getLabel("suma"))) > 0:
            app.setLabel("suma", (int(app.getLabel("suma")))-1)

    if btn == "Wyczyść koszyk":
        app.clearListBox("koszyk")
        app.setLabel("suma", 0)

    if btn == "Zapłać":
        Check2(0)

    if btn == "Zapłać za wszystkie":
        Check2(1)

    if btn == "Wpłać":
        x = ticketmachine.zwroc_wartosci(1)
        y = [0 for _ in range(14)] #[0] * 14

        y[0] = app.getEntry("0.01zł")
        y[1] = app.getEntry("0.02zł")
        y[2] = app.getEntry("0.05zł")
        y[3] = app.getEntry("0.10zł")
        y[4] = app.getEntry("0.20zł")
        y[5] = app.getEntry("0.50zł")
        y[6] = app.getEntry("1.00zł")
        y[7] = app.getEntry("2.00zł")
        y[8] = app.getEntry("5.00zł")
        y[9] = app.getEntry("10.00zł")
        y[10] = app.getEntry("20.00zł")
        y[11] = app.getEntry("50.00zł")
        y[12] = app.getEntry("100.00zł")
        y[13] = app.getEntry("200.00zł")
        licznik = 0
        for i in y:
            if (float(i).is_integer() and (int(i) >= 0)):
                licznik += 1
                i = int(i)
            else:
                i = int(0)
                app.warningBox("Błąd", "Proszę podać wartośći całkowite, większe lub równe zeru!")
                break

        if(licznik == 14):
            h = ticketmachine.zwroc_slownik(2)
            stara = list(h.values())
            nowa = y

            y = [a + b for a, b in zip(stara, nowa)] # list comprehension
            ticketmachine.wplataP(y)
            ticketmachine.zmiana()

            update()
        update_label()

    if btn == "Zwróć Monety":
        ticketmachine.zwrot()
        update()

        update_label()

app = gui("Automat Biletowy")
app.setResizable(canResize=True)
app.startPagedWindow("Automat Biletowy")
app.startPage()
app.setSticky("news")
app.setExpand("both")
app.setPadding([2,2])

#Ustawiam Tło
app.setBg("grey")

#Dodaje Tytuly. Tworze menu (Grid Layout )
app.addLabel("title1", "Prosze wybrać bilety: ", 0, 0, colspan=3)
app.addLabel("b1", "Bilety: ", 1, 0)
app.addLabel("b2", "Ulgowe: ", 1, 1)
app.addLabel("b3", "Normalne: ", 1, 2)
app.addLabel("czas1", "20-minutowe", 2, 0)
app.addLabel("czas2", "40-minutowe", 3, 0)
app.addLabel("czas3", "60-minutowe", 4, 0)
app.addLabel("whitebox3", " ", 7, 2)
app.addLabel("il_bil", " ", 5, 1)
app.addEmptyLabel("suma23", 9, 1)
app.addEmptyLabel("suma", 8, 0)
app.addEmptyLabel("suma4", 5, 0)
app.addLabel("liczba_biletow", "Liczba Biletow: ", 7, 0)
app.addLabel("Do_zapłaty", "Do Zapłaty: ", 7, 1)
app.addEmptyLabel("il_biletow433", 10, 0)
app.addEmptyLabel("il_biletow5352", 11, 1)
app.addEmptyLabel("il_biletow1262465", 10, 1)
app.setLabel("suma", "0")
app.addEmptyLabel("do_zapl", 8, 1)

app.addListBox("koszyk",[], 13, 0,colspan=2)
app.setListBoxMulti("koszyk", multi=True)


#Dodaje przyciski
app.addButton(item[0].returnName(), press, 2, 1)
app.addButton(item[1].returnName(), press, 2, 2)
app.addButton(item[2].returnName(), press, 3, 1)
app.addButton(item[3].returnName(), press, 3, 2)
app.addButton(item[4].returnName(), press, 4, 1)
app.addButton(item[5].returnName(), press, 4, 2)
app.addButton("Usuń wybrany bilet", press, 12, 0)
app.addButton("Wyczyść koszyk", press, 12, 1)
app.addButton("Zapłać", press, 13, 2)
app.addButton("Zapłać za wszystkie", press, 14, 2)
app.addButton("Cena wybranych biletów", press, 14, 0)
app.addButton("Cena wszystkich biletów", press, 14, 1)

#Kolorowanie/Czcionki itd itp
app.getLabelWidget("title1").config(font=("Sans Serif", "22", "bold"))
app.getLabelWidget("b1").config(font=("Sans Serif", "15", "bold"))
app.getLabelWidget("b2").config(font=("Sans Serif", "15", "bold"))
app.getLabelWidget("b3").config(font=("Sans Serif", "15", "bold"))
app.getLabelWidget("czas1").config(font=("Sans Serif", "14"))
app.getLabelWidget("czas2").config(font=("Sans Serif", "14"))
app.getLabelWidget("czas3").config(font=("Sans Serif", "14"))
app.setLabelHeights("b1", 2)
app.setLabelHeights("b2", 3)
app.setLabelHeights("b3", 3)
app.getLabelWidget("liczba_biletow").config(font=("Sans Serif", "15", "bold"))
app.getLabelWidget("suma").config(font=("Sans Serif", "15", "bold"))
app.getLabelWidget("Do_zapłaty").config(font=("Sans Serif", "15", "bold"))
app.getLabelWidget("do_zapl").config(font=("Sans Serif", "15", "bold"))


app.stopPage()

#DRUGA STRONA
app.startPage()
app.setBg("grey")
app.setSticky("news")
app.setExpand("both")
app.setPadding([1,1])

#Dodaje Tytuly. Tworze menu (Grid Layout )
app.addLabel("title2", " Wpłać monety: ", 0, 0)
app.addLabel("Zaplata", "Do Zaplaty: ", 1, 0)
app.addEmptyLabel("do_zapl2", 2, 0)
app.addLabel("title3", "Wpłacono: ", 3, 0)
app.addEmptyLabel("wplacone", 4, 0)
app.setPadding([1,1])
#Przyciski na monety:
app.addLabel("label1", "0.01 zł",0,4)
app.addNumericEntry("0.01zł",0,5)
app.setEntryDefault("0.01zł", "ilosc")

app.addLabel("label2", "0.02 zł",1,4)
app.addNumericEntry("0.02zł",1,5)
app.setEntryDefault("0.02zł", "ilosc")

app.addLabel("label3", "0.05 zł",2,4)
app.addNumericEntry("0.05zł",2,5)
app.setEntryDefault("0.05zł", "ilosc")

app.addLabel("label4", "0.10 zł",3,4)
app.addNumericEntry("0.10zł",3,5)
app.setEntryDefault("0.10zł", "ilosc")

app.addLabel("label5", "0.20 zł", 4, 4)
app.addNumericEntry("0.20zł", 4, 5)
app.setEntryDefault("0.20zł", "ilosc")

app.addLabel("label6", "0.50 zł", 5, 4)
app.addNumericEntry("0.50zł", 5, 5)
app.setEntryDefault("0.50zł", "ilosc")

app.addLabel("label7", "1.00 zł", 6, 4)
app.addNumericEntry("1.00zł", 6, 5)
app.setEntryDefault("1.00zł", "ilosc")

app.addLabel("label8", "2.00 zł",0,7)
app.addNumericEntry("2.00zł",0,8)
app.setEntryDefault("2.00zł", "ilosc")

app.addLabel("label9", "5.00 zł",1,7)
app.addNumericEntry("5.00zł",1,8)
app.setEntryDefault("5.00zł", "ilosc")

app.addLabel("label10", "10.00 zł",2,7)
app.addNumericEntry("10.00zł",2,8)
app.setEntryDefault("10.00zł", "ilosc")

app.addLabel("label11", "20.00 zł",3,7)
app.addNumericEntry("20.00zł",3,8)
app.setEntryDefault("20.00zł", "ilosc")

app.addLabel("label12", "50.00 zł",4,7)
app.addNumericEntry("50.00zł",4,8)
app.setEntryDefault("50.00zł", "ilosc")

app.addLabel("label13", "100.00 zł",5,7)
app.addNumericEntry("100.00zł",5,8)
app.setEntryDefault("100.00zł", "ilosc")

app.addLabel("label14", "200.00 zł",6,7)
app.addNumericEntry("200.00zł",6,8)
app.setEntryDefault("200.00zł", "ilosc")

app.addButton("Wpłać", press, 7, 7)
app.addButton("Zwróć Monety", press, 7, 8)

app.setPadding([2,2])
#Kolorowanie/Czcionki itd itp
app.getLabelWidget("title2").config(font=("Sans Serif", "22", "bold"))
app.getLabelWidget("Zaplata").config(font=("Sans Serif", "13", "bold"))
app.getLabelWidget("do_zapl2").config(font=("Sans Serif", "13", "bold"))
app.getLabelWidget("title3").config(font=("Sans Serif", "13", "bold"))
app.getLabelWidget("suma4").config(font=("Sans Serif", "13", "bold"))
app.getLabelWidget("wplacone").config(font=("Sans Serif", "13", "bold"))

app.stopPage()

#TRZECIA STRONA
app.startPage()
app.setBg("grey")
app.setSticky("news")
app.setExpand("both")
app.setPadding([2,2])

app.addEmptyLabel("automat_stan", 0, 0)
app.addLabel("Stan automatu", " ", 3, 0)
app.addLabel("wrzucone_pinionszki", " ", 3, 1)
app.getLabelWidget("automat_stan").config(font=("Sans Serif", "15", "bold"))
app.getLabelWidget("Stan automatu").config(font=("Sans Serif", "15", "bold"))
app.getLabelWidget("wrzucone_pinionszki").config(font=("Sans Serif", "15", "bold"))

app.stopPage()
app.stopPagedWindow()
app.go()