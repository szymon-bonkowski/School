import math  # Import modułu math dla operacji matematycznych, np. obliczeń sqrt

def dzielniki_naturalne(n: int) -> list:
    lst = []  # Inicjalizacja pustej listy dla dzielników
    i = 1   # Ustawienie pierwszej liczby do sprawdzenia jako dzielnika
    while i < n:  # Sprawdzenie wszystkich liczb od 1 do n-1
        if n % i == 0:
            lst.append(i)  # Jeśli i dzieli n, dodaj go do listy dzielników
        i += 1  # Przejście do następnej liczby
    return lst  # Zwraca listę dzielników liczby n

def suma(lst: list) -> float:
    s = 0  # Inicjalizacja sumy
    for el in lst:  
        s += el  # Dodajemy każdy element z listy do sumy s
    return s  # Zwraca obliczoną sumę elementów listy

def czy_to_liczba_doskonala(n: int) -> bool:
    if n <= 1:
        return False  # Liczby mniejsze lub równe 1 nie mogą być liczbami doskonałymi
    elif suma(dzielniki_naturalne(n)) == n:
        return True  # Jeśli suma dzielników (pomniejszych niż n) jest równa n, to n jest liczbą doskonałą
    return False  # W przeciwnym wypadku n nie jest liczbą doskonałą

def czy_pierwsza(n: int) -> bool:
    if n < 2:
        return False  # Liczby mniejsze niż 2 nie są pierwsze
    elif n == 2:
        return True  # 2 jest liczbą pierwszą
    elif n % 2 == 0:
        return False  # Każda parzysta liczba większa od 2 nie jest pierwsza
    i = 3  # Rozpoczynamy sprawdzanie od 3
    while i <= math.sqrt(n):  # Sprawdzamy dzielniki do pierwiastka z n
        if n % i == 0:
            return False  # Znaleziono dzielnik, n nie jest liczbą pierwszą
        i += 2  # Sprawdzamy tylko nieparzyste liczby
    return True  # Jeśli żaden dzielnik nie został znaleziony, n jest liczbą pierwszą

print("Liczby doskonałe w zakresie 1-10000:")
for i in range(1, 10001):
    if czy_to_liczba_doskonala(i):
        # Dla każdej liczby, która jest doskonała, wypisz:
        # - liczbę doskonałą (i)
        # - jej dzielniki
        # - sumę dzielników (która powinna równać się liczbie doskonałej)
        print(f"{i} | Dzielniki: {dzielniki_naturalne(i)} | Suma: {suma(dzielniki_naturalne(i))}")

print("\nLiczby pierwsze w zakresie 1-100:")
licznik = 0  # Inicjalizacja licznika znalezionych liczb pierwszych
for i in range(1, 101):
    if czy_pierwsza(i):
        print(f"{i} to liczba pierwsza")  # Jeśli liczba i jest pierwsza, wypisz odpowiednią informację
        licznik += 1  # Zwiększ licznik liczb pierwszych
print(f"Łączna liczba liczb pierwszych: {licznik}")  # Wypisz łączną liczbę znalezionych liczb pierwszych