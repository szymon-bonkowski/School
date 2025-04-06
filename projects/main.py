from projects.library import wyswietl_biblioteke, dodaj_ksiazke, usun_ksiazke, edytuj_ksiazke
from storage import zapisz_biblioteke, wczytaj_biblioteke

PLIK_BIBLIOTEKA = "biblioteka.json"

def main():
    biblioteka = wczytaj_biblioteke(PLIK_BIBLIOTEKA)
    
    while True:
        print("\nDostępne opcje:")
        print("1. Wyświetl bibliotekę")
        print("2. Dodaj książkę")
        print("3. Usuń książkę")
        print("4. Edytuj książkę")
        print("5. Zapisz i wyjdź")
        wybor = input("Wybierz opcję: ")
        
        if wybor == "1":
            wyswietl_biblioteke(biblioteka)
        elif wybor == "2":
            dodaj_ksiazke(biblioteka)
        elif wybor == "3":
            usun_ksiazke(biblioteka)
        elif wybor == "4":
            edytuj_ksiazke(biblioteka)
        elif wybor == "5":
            zapisz_biblioteke(PLIK_BIBLIOTEKA, biblioteka)
            print("Zapisano zmiany. Do widzenia!")
            break
        else:
            print("Niepoprawna opcja.")

if __name__ == "__main__":
    main()