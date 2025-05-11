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
    def __init__(self, id):
        self.id = id
        self.zajeta = False

    def zajmij(self, lot):
        self.zajeta = True
        print(f"Bramka {self.id}: zadokowano lot {lot.numer_lotu}")

    def zwolnij(self, lot):
        self.zajeta = False
        print(f"Bramka {self.id}: odłączono lot {lot.numer_lotu}")

class FlotaManager:
    def __init__(self):
        self.flota = []

    def dodaj_samolot(self, samolot):
        self.flota.append(samolot)

class BramkiManager:
    def __init__(self):
        self.bramki = [Bramka(str(i)) for i in range(1, 8)]

class SamolotCore:
    def __init__(self, identyfikator, predkosc):
        self.identyfikator = identyfikator
        self.predkosc = predkosc
        self.pozycja = 0
        self.status = 'parkowanie'
        self.paliwo = 100
        self.spalanie = 2

    def start(self):
        if self.status == 'parkowanie':
            self.status = 'start'
            print(f"{self.identyfikator}: przygotowanie do startu")

    def lot(self, warunki_pogodowe):
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

    def ladowanie(self):
        if self.status == 'ladowanie':
            self.status = 'parkowanie'
            self.pozycja = 0
            print(f"{self.identyfikator}: lądowanie zakończone i zaparkowano, uzupełnianie paliwa")
            self.paliwo = 100

class SamolotPasazerski:
    def __init__(self, identyfikator, predkosc, liczba_pasazerow, pojemnosc):
        self._core = SamolotCore(identyfikator, predkosc)
        self.liczba_pasazerow = liczba_pasazerow
        self.pojemnosc = pojemnosc

    def start(self):
        self._core.start()

    def lot(self, warunki_pogodowe):
        self._core.lot(warunki_pogodowe)

    def ladowanie(self):
        self._core.ladowanie()

    def zaladuj(self):
        print(f"{self._core.identyfikator}: załadunek pasażerów {self.liczba_pasazerow}/{self.pojemnosc}")

    def rozladuj(self):
        print(f"{self._core.identyfikator}: pasażerowie opuszczają samolot")

class SamolotTowarowy:
    def __init__(self, identyfikator, predkosc, waga_ladunku, maks_ladunek):
        self._core = SamolotCore(identyfikator, predkosc)
        self.waga_ladunku = waga_ladunku
        self.maks_ladunek = maks_ladunek

    def start(self):
        self._core.start()

    def lot(self, warunki_pogodowe):
        self._core.lot(warunki_pogodowe)

    def ladowanie(self):
        self._core.ladowanie()

    def zaladuj(self):
        print(f"{self._core.identyfikator}: załadunek towaru {self.waga_ladunku}/{self.maks_ladunek} ton")

    def rozladuj(self):
        print(f"{self._core.identyfikator}: rozładunek towaru")

class Lotnisko:
    def __init__(self, nazwa):
        self._statystyki = Statystyki()
        self._flota_manager = FlotaManager()
        self._bramki_manager = BramkiManager()
        self.nazwa = nazwa
        self.aktywne_loty = []

    def zarejestruj_odlot(self):
        self._statystyki.zarejestruj_odlot()

    def zarejestruj_przylot(self):
        self._statystyki.zarejestruj_przylot()

    def zakoncz_lot(self):
        self._statystyki.zakoncz_lot()

    def wyswietl(self):
        self._statystyki.wyswietl()

    def dodaj_samolot(self, samolot):
        self._flota_manager.dodaj_samolot(samolot)
    
    def get_bramki(self):
        return self._bramki_manager.bramki

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

class Lot:
    def __init__(self, numer_lotu, samolot, punkt_startu, cel):
        self.numer_lotu = numer_lotu
        self.samolot = samolot 
        self.punkt_startu = punkt_startu
        self.cel = cel
        self.faza = 0
        self.zakonczony = False
        self.bramka = None

    def inicjalizuj(self, lotnisko):
        print(f"Lot {self.numer_lotu}: przygotowanie faza init")
        self.samolot.zaladuj()
        self.samolot.start()
        self.samolot._core.status = 'lot' 
        self.faza = 1

    def aktualizuj(self, lotnisko, warunki_pogodowe):
        if self.faza == 0:
            self.inicjalizuj(lotnisko)
        elif self.faza == 1:
            self.samolot.lot(warunki_pogodowe)
            if self.samolot._core.pozycja >= 100 or self.samolot._core.status == 'ladowanie':
                print(f"Lot {self.numer_lotu}: osiągnięto cel lub potrzeba lądowania")
                self.samolot._core.status = 'ladowanie'
                self.faza = 2
        elif self.faza == 2:
            self.samolot.ladowanie()
            self.samolot.rozladuj()
            bramka_przydzielona = False
            for br in lotnisko.get_bramki(): 
                if not br.zajeta:
                    self.bramka = br
                    br.zajmij(self)
                    bramka_przydzielona = True
                    break
            print(f"Lot {self.numer_lotu}: zakończony")
            self.zakonczony = True

class WarunkiPogodowe:
    def __init__(self):
        self.status = 'slonecznie'
        self.temperatura = 20

    def aktualizuj(self, krok_symulacji):
        if krok_symulacji % 8 == 0:
            self.status = 'burza'
            self.temperatura -= 12
        elif krok_symulacji % 5 == 0:
            self.status = 'pochmurno'
            self.temperatura -= 3
        else:
            self.status = 'slonecznie'
            self.temperatura += 2

def uruchom_symulacje():
    lotnisko = Lotnisko('Okecie')
    warunki = WarunkiPogodowe()
    samoloty_w_symulacji = []
    for i in range(8):
        if i % 2 == 0:
            samolot = SamolotPasazerski(f'S{i+100}', 10+i, 100+i*5, 150+i*10)
        else:
            samolot = SamolotTowarowy(f'S{i+100}', 10+i, 20+i*3, 50+i*5)
        samoloty_w_symulacji.append(samolot)
        lotnisko.dodaj_samolot(samolot)
    destinations = ['Berlin', 'Londyn', 'Paryz', 'Amsterdam']
    loty_w_symulacji = []
    for idx, s_obj in enumerate(samoloty_w_symulacji):
        loty_w_symulacji.append(Lot(f'L{idx+1:03d}', s_obj, 'Warszawa', destinations[idx % len(destinations)]))
    for lot_obj in loty_w_symulacji:
        lotnisko.zaplanuj_odlot(lot_obj)
        lotnisko.zaplanuj_przylot(lot_obj)
    for krok_symulacji in range(1, 81):
        warunki.aktualizuj(krok_symulacji)
        lotnisko.krok(warunki)

if __name__ == '__main__':
    uruchom_symulacje()