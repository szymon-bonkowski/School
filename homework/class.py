class klasa_a:
    def __init__(self, x, y, wart, liczba, tekst, flaga, n, zmienprz, lista, slownik):
        self.x = x
        self.y = y
        self.wart = wart
        self.liczba = liczba
        self.tekst = tekst
        self.flaga = flaga
        self.n = n
        self.zmienprz = zmienprz
        self.lista = lista
        self.slownik = slownik

    def pobierz_x(self):
        return f"wartość x: {self.x}"

    def suma_wartosci(self):
        return f"suma y + wartosc: " + str(self.y + self.wart)

    def inkrementuj(self):
        self.liczba += 1
        return f"zwiększono liczba o 1, teraz wynosi " + str(self.liczba)

    def pierwsze5(self):
        return f"lista pierwszych 5: {[self.x, self.y, self.wart, self.liczba, self.tekst]}"

    def sprawdz_typ(self):
        return f"typ flaga to " + str(type(self.flaga))

    def kwadrat(self):
        return f"n do kwadratu: " + str(self.n ** 2)

    def wszystko(self):
        return f"wszystko: {[self.x, self.y, self.wart, self.liczba, self.tekst, self.flaga, self.n, self.zmienprz, self.lista, self.slownik]}"


class klasa_b:
    def __init__(self, a, b, c, d, e, f, g, h, i, j):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        self.i = i
        self.j = j

    def metoda1(self):
        return f"a to: {self.a}"

    def metoda_2(self):
        return f"b i c to: {self.b}, {self.c}"

    def wielkie(self):
        self.d = str(self.d).upper()
        return f"d na wielkie litery: " + self.d

    def dlugosc(self):
        return "długość e: " + str(len(str(self.e)))

    def pomnoz(self):
        return "f * 10 = " + str(self.f * 10)

    def dzielenie(self):
        if type(self.g) == int or type(self.g) == float:
            return "g / 2 = " + str(self.g / 2)
        else:
            return "g nie jest liczbą"

    def pokaz_wszystkie(self):
        return "wszystko klasa_b: " + str([self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.i, self.j])


class klasa_c:
    def __init__(self, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.p7 = p7
        self.p8 = p8
        self.p9 = p9
        self.p10 = p10

    def pokaz_1(self):
        return "p1: " + str(self.p1)

    def sprawdz(self):
        if self.p2 > 0:
            return "p2 dodatnie (" + str(self.p2) + ")"
        else:
            return "p2 nie dodatnie (" + str(self.p2) + ")"

    def dodaj_5(self):
        self.p3 = self.p3 + 5
        return "p3 + 5: " + str(self.p3)

    def polacz(self):
        return "razem p4 i p5: " + str(self.p4) + str(self.p5)

    def pobierz_wartosci(self):
        return "p6, p7, p8: " + str(self.p6) + ", " + str(self.p7) + ", " + str(self.p8)

    def zrob_liste(self):
        self.p9 = list(str(self.p9))
        return "p9 lista: " + str(self.p9)

    def wszystkie_wartosci(self):
        return "wszystko: " + str([self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.p9, self.p10])


def uruchom():
    ob1 = klasa_a(1, 2, 3, 4, "jakis tekst", True, 5, 8.9, [1, 2], {"klucz": "wartosc"})
    ob2 = klasa_a(10, 20, 30, 40, "cos tam", False, 7, 1.1, [5, 6], {"foo": "bar"})
    ob3 = klasa_a(100, 200, 300, 400, "python", True, 11, 2.2, [9, 0], {"xyz": 123})

    obiektB1 = klasa_b("Ala", "ma", "kota", "dom", 123, 5, 3.14, True, None, "koniec")
    obiektB2 = klasa_b("Test", "B2", "B3", "napis", "coś", 10, 42, False, 99, "X")
    obiektB3 = klasa_b("Jan", "Nowak", "Python", "Krakow", "Info", 100, 256, 3.14, 0, "Ostatni")

    c1 = klasa_c(1, 2, 3, "c4", "c5", 6, 7, 8, "txt9", 10)
    c2 = klasa_c(0, -5, 50, 100, 200, "abc", "def", "ghi", "tekst", 99)
    c3 = klasa_c(5, 10, 15, True, False, [1, 2, 3], {"k": "w"}, 3.14, "czesc", "swiat")

    print(ob1.pobierz_x())
    print(ob1.inkrementuj())
    print(ob1.wszystko())

    print(obiektB1.wielkie())
    print(obiektB1.pokaz_wszystkie())

    print(c2.sprawdz())
    print(c2.dodaj_5())
    print(c2.wszystkie_wartosci())


if __name__ == "__main__":
    uruchom()