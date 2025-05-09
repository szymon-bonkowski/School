class SamolotPasazerskiCzesc:
    def __init__(self, pax_cap):
        self.pax_cap = pax_cap
    def lataj_akcja(self, ident):
        return f"{ident} startuje, {self.pax_cap} ludzików na pokładzie"
    def laduj_akcja(self, ident):
        return f"{ident} lądowanie ok"
    def stan_info(self, ident, czy_leci):
        status_lotu = "w powietrzu" if czy_leci else "na glebie"
        return f"typ pasazerski {ident}, {status_lotu}"
    def przyjmij_pasazerow_akcja(self, ident):
        return f"{ident} wpuszczanie na pokład"
    def czysc_kabine_akcja(self, ident):
        return f"{ident} sprzątanie"
    def ogloszenie_akcja(self, ident):
        return f"{ident} witamy na pokładzie, lecimy"

class SamolotTowarowyCzesc:
    def __init__(self, waga_ladunku):
        self.waga_ladunku = waga_ladunku
    def lataj_akcja(self, ident):
        return f"{ident} leci z ładunkiem {self.waga_ladunku}kg"
    def laduj_akcja(self, ident):
        return f"{ident} po wylądowaniu"
    def stan_info(self, ident, czy_leci):
        status_lotu = "w powietrzu" if czy_leci else "na glebie"
        return f"transportowiec {ident}, {status_lotu}"
    def zaladuj_towar_akcja(self, ident):
        return f"{ident} ładowanie towaru"
    def sprawdz_drzwi_akcja(self, ident):
        return f"{ident} drzwi ładowni ok"
    def sprawdz_ladunek_akcja(self, ident):
         return f"{ident} ładunek jest"

class SmiglowiecCzesc:
    def __init__(self, wirnik_rozm):
        self.wirnik_rozm = wirnik_rozm
    def lataj_akcja(self, ident):
        return f"{ident} idzie w górę pionowo (wirnik {self.wirnik_rozm}m)"
    def laduj_akcja(self, ident):
        return f"{ident} lądowanie pionowe"
    def stan_info(self, ident, czy_leci):
        status_lotu = "w powietrzu" if czy_leci else "na glebie"
        return f"helikopter {ident}, {status_lotu}"
    def sprawdz_wirnik_akcja(self, ident):
         return f"{ident} wirnik sprawdzony"
    def zawis_akcja(self, ident):
        return f"{ident} wisi w powietrzu"
    def swiatla_akcja(self, ident):
        return f"{ident} światła pozycyjne włączone"

class WodnosamolotCzesc:
    def __init__(self, czy_na_wode):
        self.czy_na_wode = czy_na_wode
    def lataj_akcja(self, ident):
        start_info = "z wody" if self.czy_na_wode else "z pasa"
        return f"{ident} startuje {start_info}"
    def laduj_akcja(self, ident):
        laduj_info = "na wodzie" if self.czy_na_wode else "na lądzie"
        return f"{ident} ląduje {laduj_info}"
    def stan_info(self, ident, czy_leci):
        status_lotu = "w powietrzu" if czy_leci else "na ziemi/wodzie"
        return f"wodnosamolot {ident}, {status_lotu}"
    def plywaj_po_wodzie_akcja(self, ident, czy_leci_status):
        if not czy_leci_status and self.czy_na_wode:
             return f"{ident} unosi się na wodzie"
        elif czy_leci_status:
             return f"{ident} jest w locie, nie pływa"
        else:
             return f"{ident} jest na lądzie"
    def podwozie_wodne_akcja(self, ident):
        if self.czy_na_wode:
            return f"{ident} chowanie pływaków"
        return f"{ident} nie mam pływaków"

class MaszynaLotnicza:
    def __init__(self, ident, czesc_maszyny):
        self.ident = ident
        self.czesc_maszyny = czesc_maszyny
        self.czy_leci = False
    def lataj(self):
        self.czy_leci = True
        return self.czesc_maszyny.lataj_akcja(self.ident)
    def laduj(self):
        self.czy_leci = False
        return self.czesc_maszyny.laduj_akcja(self.ident)
    def stan(self):
        return self.czesc_maszyny.stan_info(self.ident, self.czy_leci)
    def sprawdz_silnik(self):
         return f"{self.ident}: sprawdzam silnik"
    def przyjmij_pasazerow(self):
         if hasattr(self.czesc_maszyny, 'przyjmij_pasazerow_akcja'):
             return self.czesc_maszyny.przyjmij_pasazerow_akcja(self.ident)
         return f"{self.ident}: brak akcji przyjmij pasażerów"
    def czysc_kabine(self):
         if hasattr(self.czesc_maszyny, 'czysc_kabine_akcja'):
             return self.czesc_maszyny.czysc_kabine_akcja(self.ident)
         return f"{self.ident}: brak akcji czysc kabinę"
    def ogloszenie(self):
        if hasattr(self.czesc_maszyny, 'ogloszenie_akcja'):
            return self.czesc_maszyny.ogloszenie_akcja(self.ident)
        return f"{self.ident}: brak ogłoszeń"
    def zaladuj_towar(self):
         if hasattr(self.czesc_maszyny, 'zaladuj_towar_akcja'):
             return self.czesc_maszyny.zaladuj_towar_akcja(self.ident)
         return f"{self.ident}: brak akcji załaduj towar"
    def sprawdz_drzwi(self):
        if hasattr(self.czesc_maszyny, 'sprawdz_drzwi_akcja'):
            return self.czesc_maszyny.sprawdz_drzwi_akcja(self.ident)
        return f"{self.ident}: brak akcji sprawdz drzwi"
    def sprawdz_ladunek(self):
         if hasattr(self.czesc_maszyny, 'sprawdz_ladunek_akcja'):
             return self.czesc_maszyny.sprawdz_ladunek_akcja(self.ident)
         return f"{self.ident}: brak akcji sprawdz ładunek"
    def sprawdz_wirnik(self):
        if hasattr(self.czesc_maszyny, 'sprawdz_wirnik_akcja'):
            return self.czesc_maszyny.sprawdz_wirnik_akcja(self.ident)
        return f"{self.ident}: brak akcji sprawdz wirnik"
    def zawis(self):
        if hasattr(self.czesc_maszyny, 'zawis_akcja'):
             return self.czesc_maszyny.zawis_akcja(self.ident)
        return f"{self.ident}: brak akcji zawis"
    def swiatla(self):
        if hasattr(self.czesc_maszyny, 'swiatla_akcja'):
            return self.czesc_maszyny.swiatla_akcja(self.ident)
        return f"{self.ident}: brak akcji włącz światła"
    def podwozie_wodne(self):
         if hasattr(self.czesc_maszyny, 'podwozie_wodne_akcja'):
             return self.czesc_maszyny.podwozie_wodne_akcja(self.ident)
         return f"{self.ident}: brak akcji podwozie wodne"
    def plywaj_po_wodzie(self):
         if hasattr(self.czesc_maszyny, 'plywaj_po_wodzie_akcja'):
             return self.czesc_maszyny.plywaj_po_wodzie_akcja(self.ident, self.czy_leci)
         return f"{self.ident}: brak akcji pływaj po wodzie"

class TerminalAkcja:
    def info_akcja(self, terminal_id):
        raise NotImplementedError("info_akcja musi byc zrobione")

class TerminalOdprawAkcja(TerminalAkcja):
    def info_akcja(self, terminal_id):
        return f"odprawa {terminal_id} tutaj się odprawiasz"

class TerminalOdlotowAkcja(TerminalAkcja):
    def info_akcja(self, terminal_id):
        return f"odloty {terminal_id} do bramek"

class TerminalPrzylotowAkcja(TerminalAkcja):
    def info_akcja(self, terminal_id):
        return f"przyloty {terminal_id} odbierz bagaż"

class TerminalObiekt:
    def __init__(self, id_terminalu, akcja_terminalu):
        self.id_terminalu = id_terminalu
        self.akcja_terminalu = akcja_terminalu
    def serwis(self):
        return self.akcja_terminalu.info_akcja(self.id_terminalu)

class PortLotniczy:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.maszyny = []
        self.terminale = []
    def dodaj_maszyne(self, maszyna):
        self.maszyny.append(maszyna)
    def dodaj_terminal(self, terminal):
        self.terminale.append(terminal)
    def pokaz_maszyny(self):
        print("lotnisko '{}': maszyny co stoją:".format(self.nazwa))
        if not self.maszyny:
            print("pusto")
            return
        for m in self.maszyny:
            print("{} -> {}".format(m.ident, m.stan()))
    def pokaz_terminale(self):
        print("lotnisko '{}': terminale:".format(self.nazwa))
        if not self.terminale:
            print("brak terminali")
            return
        for t in self.terminale:
            print("{}: {}".format(t.id_terminalu, t.serwis()))
    def operuj_loty(self):
        print("robimy operacje lotnicze:")
        if not self.maszyny:
            print("brak maszyn do operowania")
            return
        for m in self.maszyny:
            print(">>> maszyna:", m.ident)
            print(m.sprawdz_silnik())
            if isinstance(m.czesc_maszyny, SamolotPasazerskiCzesc):
                 print(m.przyjmij_pasazerow())
                 print(m.czysc_kabine())
            elif isinstance(m.czesc_maszyny, SamolotTowarowyCzesc):
                 print(m.zaladuj_towar())
                 print(m.sprawdz_drzwi())
            elif isinstance(m.czesc_maszyny, SmiglowiecCzesc):
                print(m.sprawdz_wirnik())
            elif isinstance(m.czesc_maszyny, WodnosamolotCzesc):
                print(m.podwozie_wodne())
            print(m.lataj())
            if m.czy_leci:
                if isinstance(m.czesc_maszyny, SamolotPasazerskiCzesc):
                    print(m.ogloszenie())
                elif isinstance(m.czesc_maszyny, SamolotTowarowyCzesc):
                    print(m.sprawdz_ladunek())
                elif isinstance(m.czesc_maszyny, SmiglowiecCzesc):
                    print(m.zawis())
                    print(m.swiatla())
                elif isinstance(m.czesc_maszyny, WodnosamolotCzesc):
                     print(m.plywaj_po_wodzie())
            print(m.laduj())
            print("<<< koniec dla maszyny", m.ident)
            print()

def main():
    lotnisko1 = PortLotniczy("Duże Lotnisko")
    pp1_czesc = SamolotPasazerskiCzesc(175)
    cp1_czesc = SamolotTowarowyCzesc(85000)
    heli1_czesc = SmiglowiecCzesc(15)
    sp1_czesc = WodnosamolotCzesc(True)
    pp1 = MaszynaLotnicza("BOEING737", pp1_czesc)
    cp1 = MaszynaLotnicza("ANTONOV124", cp1_czesc)
    heli1 = MaszynaLotnicza("MI8", heli1_czesc)
    sp1 = MaszynaLotnicza("TWINOTTER", sp1_czesc)
    lotnisko1.dodaj_maszyne(pp1)
    lotnisko1.dodaj_maszyne(cp1)
    lotnisko1.dodaj_maszyne(heli1)
    lotnisko1.dodaj_maszyne(sp1)
    cit1_akcja = TerminalOdprawAkcja()
    dt1_akcja = TerminalOdlotowAkcja()
    at1_akcja = TerminalPrzylotowAkcja()
    cit1 = TerminalObiekt("A-jeden", cit1_akcja)
    dt1 = TerminalObiekt("B-dwa", dt1_akcja)
    at1 = TerminalObiekt("C-trzy", at1_akcja)
    lotnisko1.dodaj_terminal(cit1)
    lotnisko1.dodaj_terminal(dt1)
    lotnisko1.dodaj_terminal(at1)
    lotnisko1.pokaz_maszyny()
    lotnisko1.pokaz_terminale()
    lotnisko1.operuj_loty()
    print("stan maszyn po operacjach:")
    lotnisko1.pokaz_maszyny()

if __name__ == "__main__":
    main()