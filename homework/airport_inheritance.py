class Statystyki:
    def __init__(self):
        self.odloty = 0
        self.przyloty = 0
        self.zakonczone_loty = 0

    def zarejestruj_odlot(self):
        self.odloty += 1

    def zarejestruj_przylot(self):
        self.przyloty += 1

    def zakoncz_lot(self):
        self.zakonczone_loty += 1

    def wyswietl(self):
        print(f"Statystyki: odloty={self.odloty}, przyloty={self.przyloty}, zakończone_loty={self.zakonczone_loty}\n")

class Bramka:
    def __init__(self, id_bramki):
        self.id = id_bramki
        self.zajeta = False

    def zajmij(self, lot):
        self.zajeta = True
        print(f"Bramka {self.id}: zadokowano lot {lot.numer_lotu}")

    def zwolnij(self, lot):
        self.zajeta = False
        print(f"Bramka {self.id}: odłączono lot {lot.numer_lotu}")

class FlotaMixin:
    def __init__(self):
        self.flota = []

    def dodaj_samolot(self, samolot):
        self.flota.append(samolot)

class BramkiMixin:
    def __init__(self):
        self.bramki = [Bramka(str(i)) for i in range(1, 8)]

class Lotnisko(Statystyki, FlotaMixin, BramkiMixin):
    def __init__(self, nazwa):
        Statystyki.__init__(self)
        FlotaMixin.__init__(self)
        BramkiMixin.__init__(self)
        self.nazwa = nazwa
        self.aktywne_loty = []

    def zaplanuj_odlot(self, lot):
        self.aktywne_loty.append(lot)
        print(f"[{self.nazwa}] Zaplanowano odlot: {lot.numer_lotu} z {lot.punkt_startu} do {lot.cel}")
        self.zarejestruj_odlot()

    def zaplanuj_przylot(self, lot):
        self.aktywne_loty.append(lot)
        print(f"[{self.nazwa}] Zaplanowano przylot: {lot.numer_lotu} z {lot.punkt_startu} do {lot.cel}")
        self.zarejestruj_przylot()

    def krok(self, warunki_pogodowe):
        print(f"--- [{self.nazwa}] Symulacja kroku przy pogodzie: {warunki_pogodowe.status}, temp: {warunki_pogodowe.temperatura}C ---")
        for lot_obj in list(self.aktywne_loty):
            lot_obj.aktualizuj(self, warunki_pogodowe)
            if lot_obj.zakonczony:
                self.aktywne_loty.remove(lot_obj)
                self.zakoncz_lot()
        self.wyswietl()

class Samolot:
    def __init__(self, identyfikator, predkosc):
        self.identyfikator = identyfikator
        self.predkosc = predkosc
        self.pozycja = 0
        self.status = 'parkowanie'
        self.paliwo = 100
        self.spalanie = 2

    def start_samolotu(self):
        if self.status == 'parkowanie':
            self.status = 'start'
            print(f"{self.identyfikator}: przygotowanie do startu")

    def lot_w_powietrzu(self, warunki_pogodowe):
        if self.status == 'lot':
            if self.paliwo <= 0:
                print(f"{self.identyfikator}: brak paliwa, awaryjne lądowanie")
                self.status = 'ladowanie'
                return
            if warunki_pogodowe.status == 'burza':
                print(f"{self.identyfikator}: oczekiwanie na poprawę pogody")
            else:
                self.pozycja += self.predkosc
                self.paliwo -= self.spalanie
                print(f"{self.identyfikator}: w powietrzu, pozycja {self.pozycja}, paliwo {self.paliwo}")

    def ladowanie_samolotu(self):
        if self.status == 'ladowanie':
            self.status = 'parkowanie'
            self.pozycja = 0
            print(f"{self.identyfikator}: lądowanie zakończone i zaparkowano, uzupełnianie paliwa")
            self.paliwo = 100

    def zaladuj(self):
        pass

    def rozladuj(self):
        pass

class Lot(Samolot):
    def __init__(self, numer_lotu, identyfikator_samolotu, predkosc_samolotu, punkt_startu, cel):
        super().__init__(identyfikator_samolotu, predkosc_samolotu)
        self.numer_lotu = numer_lotu
        self.punkt_startu = punkt_startu
        self.cel = cel
        self.faza = 0
        self.zakonczony = False
        self.bramka_przydzielona = None

    def inicjalizuj(self, lotnisko):
        print(f"Lot {self.numer_lotu}: przygotowanie faza init")
        self.zaladuj()
        self.start_samolotu()
        self.status = 'lot'
        self.faza = 1

    def aktualizuj(self, lotnisko, warunki_pogodowe):
        if self.faza == 0:
            self.inicjalizuj(lotnisko)
        elif self.faza == 1:
            self.lot_w_powietrzu(warunki_pogodowe)
            if self.pozycja >= 100 or self.status == 'ladowanie':
                print(f"Lot {self.numer_lotu}: osiągnięto cel lub potrzeba lądowania")
                self.status = 'ladowanie'
                self.faza = 2
        elif self.faza == 2:
            self.ladowanie_samolotu()
            self.rozladuj()
            for br in lotnisko.bramki:
                if not br.zajeta:
                    self.bramka_przydzielona = br
                    br.zajmij(self)
                    break
            print(f"Lot {self.numer_lotu}: zakończony")
            self.zakonczony = True

class PasazerskiLot(Lot):
    def __init__(self, numer_lotu, identyfikator_samolotu, predkosc_samolotu, punkt_startu, cel, liczba_pasazerow, pojemnosc):
        super().__init__(numer_lotu, identyfikator_samolotu, predkosc_samolotu, punkt_startu, cel)
        self.liczba_pasazerow = liczba_pasazerow
        self.pojemnosc = pojemnosc

    def zaladuj(self):
        print(f"{self.identyfikator}: załadunek pasażerów {self.liczba_pasazerow}/{self.pojemnosc}")

    def rozladuj(self):
        print(f"{self.identyfikator}: pasażerowie opuszczają samolot")

class TowarowyLot(Lot):
    def __init__(self, numer_lotu, identyfikator_samolotu, predkosc_samolotu, punkt_startu, cel, waga_ladunku, maks_ladunek):
        super().__init__(numer_lotu, identyfikator_samolotu, predkosc_samolotu, punkt_startu, cel)
        self.waga_ladunku = waga_ladunku
        self.maks_ladunek = maks_ladunek

    def zaladuj(self):
        print(f"{self.identyfikator}: załadunek towaru {self.waga_ladunku}/{self.maks_ladunek} ton")

    def rozladuj(self):
        print(f"{self.identyfikator}: rozładunek towaru")

class WarunkiPogodowe:
    def __init__(self):
        self.status = 'slonecznie'
        self.temperatura = 20

    def aktualizuj(self, krok):
        if krok % 8 == 0:
            self.status = 'burza'
            self.temperatura -= 12
        elif krok % 5 == 0:
            self.status = 'pochmurno'
            self.temperatura -= 3
        else:
            self.status = 'slonecznie'
            self.temperatura += 2

def uruchom_symulacje():
    lotnisko = Lotnisko('Okecie')
    warunki = WarunkiPogodowe()
    loty_do_zaplanowania = []
    destinations = ['Berlin', 'Londyn', 'Paryz', 'Amsterdam']

    for i in range(8):
        ident_samolotu = f'S{i+100}'
        pr_samolotu = 10 + i
        num_lotu = f'L{i+1:03d}'
        cel_lotu = destinations[i % len(destinations)]

        if i % 2 == 0:
            lot_obj = PasazerskiLot(
                numer_lotu=num_lotu,
                identyfikator_samolotu=ident_samolotu,
                predkosc_samolotu=pr_samolotu,
                punkt_startu='Warszawa',
                cel=cel_lotu,
                liczba_pasazerow=100 + i * 5,
                pojemnosc=150 + i * 10
            )
        else:
            lot_obj = TowarowyLot(
                numer_lotu=num_lotu,
                identyfikator_samolotu=ident_samolotu,
                predkosc_samolotu=pr_samolotu,
                punkt_startu='Warszawa',
                cel=cel_lotu,
                waga_ladunku=20 + i * 3,
                maks_ladunek=50 + i * 5
            )
        loty_do_zaplanowania.append(lot_obj)
        lotnisko.dodaj_samolot(lot_obj)

    for lot_obj in loty_do_zaplanowania:
        lotnisko.zaplanuj_odlot(lot_obj)
        lotnisko.zaplanuj_przylot(lot_obj)

    for krok in range(1, 81):
        warunki.aktualizuj(krok)
        lotnisko.krok(warunki)

if __name__ == '__main__':
    uruchom_symulacje()