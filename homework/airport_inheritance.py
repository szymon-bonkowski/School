class MaszynaLotnicza:
    def __init__(self, ident):
        self.ident = ident
        self.czy_leci = False
    def lataj(self):
        self.czy_leci = True
    def laduj(self):
        self.czy_leci = False
    def stan(self):
        raise NotImplementedError("stan musi byc zrobione")
    def sprawdz_silnik(self):
        return f"{self.ident}: sprawdzam silnik"

class SamolotPasazerski(MaszynaLotnicza):
    def __init__(self, ident, pax_cap):
        super().__init__(ident)
        self.pax_cap = pax_cap
    def lataj(self):
        super().lataj()
        return f"{self.ident} startuje, {self.pax_cap} ludzików na pokładzie"
    def laduj(self):
        super().laduj()
        return f"{self.ident} lądowanie ok"
    def stan(self):
        status_lotu = "w powietrzu" if self.czy_leci else "na glebie"
        return f"typ pasazerski {self.ident}, {status_lotu}"
    def przyjmij_pasazerow(self):
        return f"{self.ident} wpuszczanie na pokład"
    def czysc_kabine(self):
        return f"{self.ident} sprzątanie"
    def ogloszenie(self):
        return f"{self.ident} witamy na pokładzie, lecimy"

class SamolotTowarowy(MaszynaLotnicza):
    def __init__(self, ident, waga_ladunku):
        super().__init__(ident)
        self.waga_ladunku = waga_ladunku
    def lataj(self):
        super().lataj()
        return f"{self.ident} leci z ładunkiem {self.waga_ladunku}kg"
    def laduj(self):
        super().laduj()
        return f"{self.ident} po wylądowaniu"
    def stan(self):
        status_lotu = "w powietrzu" if self.czy_leci else "na glebie"
        return f"transportowiec {self.ident}, {status_lotu}"
    def zaladuj_towar(self):
        return f"{self.ident} ładowanie towaru"
    def sprawdz_drzwi(self):
        return f"{self.ident} drzwi ładowni ok"
    def sprawdz_ladunek(self):
        return f"{self.ident} ładunek jest"

class Smiglowiec(MaszynaLotnicza):
    def __init__(self, ident, wirnik_rozm):
        super().__init__(ident)
        self.wirnik_rozm = wirnik_rozm
    def lataj(self):
        super().lataj()
        return f"{self.ident} idzie w górę pionowo (wirnik {self.wirnik_rozm}m)"
    def laduj(self):
        super().laduj()
        return f"{self.ident} lądowanie pionowe"
    def stan(self):
        status_lotu = "w powietrzu" if self.czy_leci else "na glebie"
        return f"helikopter {self.ident}, {status_lotu}"
    def sprawdz_wirnik(self):
        return f"{self.ident} wirnik sprawdzony"
    def zawis(self):
        return f"{self.ident} wisi w powietrzu"
    def swiatla(self):
        return f"{self.ident} światła pozycyjne włączone"

class Wodnosamolot(MaszynaLotnicza):
    def __init__(self, ident, czy_na_wode):
        super().__init__(ident)
        self.czy_na_wode = czy_na_wode
    def lataj(self):
        super().lataj()
        start_info = "z wody" if self.czy_na_wode else "z pasa"
        return f"{self.ident} startuje {start_info}"
    def laduj(self):
        super().laduj()
        laduj_info = "na wodzie" if self.czy_na_wode else "na lądzie"
        return f"{self.ident} ląduje {laduj_info}"
    def stan(self):
        status_lotu = "w powietrzu" if self.czy_leci else "na ziemi/wodzie"
        return f"wodnosamolot {self.ident}, {status_lotu}"
    def podwozie_wodne(self):
        if self.czy_na_wode:
            return f"{self.ident} chowanie pływaków"
        return f"{self.ident} nie mam pływaków"
    def plywaj_po_wodzie(self):
        if not self.czy_leci and self.czy_na_wode:
            return f"{self.ident} unosi się na wodzie"
        elif self.czy_leci:
            return f"{self.ident} jest w locie, nie pływa"
        else:
            return f"{self.ident} jest na lądzie"


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
            print("{} ({}) -> {}".format(m.ident, m.__class__.__name__, m.stan()))
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
            if isinstance(m, SamolotPasazerski):
                 print(m.przyjmij_pasazerow())
                 print(m.czysc_kabine())
            elif isinstance(m, SamolotTowarowy):
                 print(m.zaladuj_towar())
                 print(m.sprawdz_drzwi())
            elif isinstance(m, Smiglowiec):
                print(m.sprawdz_wirnik())
            elif isinstance(m, Wodnosamolot):
                print(m.podwozie_wodne())
            print(m.lataj())
            if m.czy_leci:
                if isinstance(m, SamolotPasazerski):
                    print(m.ogloszenie())
                elif isinstance(m, SamolotTowarowy):
                    print(m.sprawdz_ladunek())
                elif isinstance(m, Smiglowiec):
                    print(m.zawis())
                    print(m.swiatla())
                elif isinstance(m, Wodnosamolot):
                     print(m.plywaj_po_wodzie())
            print(m.laduj())
            print("<<< koniec dla maszyny", m.ident)
            print()

class TerminalObiekt:
    def __init__(self, id_terminalu):
        self.id_terminalu = id_terminalu
    def serwis(self):
        raise NotImplementedError("serwis musi byc zrobione")

class TerminalOdpraw(TerminalObiekt):
    def serwis(self):
        return f"odprawa {self.id_terminalu} tutaj się odprawiasz"

class TerminalOdlotow(TerminalObiekt):
    def serwis(self):
        return f"odloty {self.id_terminalu} do bramek"

class TerminalPrzylotow(TerminalObiekt):
    def serwis(self):
        return f"przyloty {self.id_terminalu} odbierz bagaż"

def main():
    lotnisko1 = PortLotniczy("Duże Lotnisko")
    pp1 = SamolotPasazerski("BOEING737", 175)
    cp1 = SamolotTowarowy("ANTONOV124", 85000)
    heli1 = Smiglowiec("MI8", 15)
    sp1 = Wodnosamolot("TWINOTTER", True)
    lotnisko1.dodaj_maszyne(pp1)
    lotnisko1.dodaj_maszyne(cp1)
    lotnisko1.dodaj_maszyne(heli1)
    lotnisko1.dodaj_maszyne(sp1)
    cit1 = TerminalOdpraw("A-jeden")
    dt1 = TerminalOdlotow("B-dwa")
    at1 = TerminalPrzylotow("C-trzy")
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