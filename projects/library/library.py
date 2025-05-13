from models import Ksiazka

def wyswietl_biblioteke(biblioteka):
    if not biblioteka:
        print("Biblioteka jest pusta.")
        return
    for ksiazka in biblioteka:
        print(f"ID: {ksiazka.id}")
        print(f"Nazwa: {ksiazka.nazwa}")
        print(f"Liczba stron: {ksiazka.liczba_stron}")
        print("-" * 30)

def dodaj_ksiazke(biblioteka):
    nazwa = input("Podaj nazwę książki: ")
    if not nazwa.strip():
        print("Nazwa książki nie może być pusta!")
        return
    liczba_stron = input("Podaj liczbę stron: ")
    try:
        liczba_stron = int(liczba_stron)
    except ValueError:
        print("Liczba stron musi być liczbą!")
        return
    nowa_ksiazka = Ksiazka(nazwa, liczba_stron)
    biblioteka.append(nowa_ksiazka)
    print("Książka została dodana.")

def usun_ksiazke(biblioteka):
    if not biblioteka:
        print("Biblioteka jest pusta. Brak książek do usunięcia.")
        return
    print("Lista książek:")
    wyswietl_biblioteke(biblioteka)
    id_ksiazki = input("Podaj ID książki do usunięcia: ")
    for ksiazka in biblioteka:
        if ksiazka.id == id_ksiazki:
            biblioteka.remove(ksiazka)
            print("Książka została usunięta.")
            return
    print("Nie znaleziono książki o podanym ID.")

def edytuj_ksiazke(biblioteka):
    if not biblioteka:
        print("Biblioteka jest pusta. Brak książek do edycji.")
        return
    print("Lista książek:")
    wyswietl_biblioteke(biblioteka)
    id_ksiazki = input("Podaj ID książki do edycji: ")
    for ksiazka in biblioteka:
        if ksiazka.id == id_ksiazki:
            print("Wybierz co chcesz edytować:")
            print("1. Nazwa")
            print("2. Liczba stron")
            wybor = input("Twój wybór: ")
            if wybor == "1":
                nowa_nazwa = input("Podaj nową nazwę: ")
                if not nowa_nazwa.strip():
                    print("Nazwa książki nie może być pusta!")
                    return
                ksiazka.nazwa = nowa_nazwa
                print("Nazwa została zaktualizowana.")
            elif wybor == "2":
                nowa_liczba = input("Podaj nową liczbę stron: ")
                try:
                    ksiazka.liczba_stron = int(nowa_liczba)
                    print("Liczba stron została zaktualizowana.")
                except ValueError:
                    print("Liczba stron musi być liczbą!")
            else:
                print("Niepoprawny wybór.")
            return
    print("Nie znaleziono książki o podanym ID.")