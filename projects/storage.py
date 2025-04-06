import json
from models import Ksiazka

def zapisz_biblioteke(plik, biblioteka):
    lista_dict = [ksiazka.to_dict() for ksiazka in biblioteka]
    with open(plik, 'w', encoding='utf-8') as f:
        json.dump(lista_dict, f, ensure_ascii=False, indent=4)

def wczytaj_biblioteke(plik):
    biblioteka = []
    try:
        with open(plik, 'r', encoding='utf-8') as f:
            lista_dict = json.load(f)
            for d in lista_dict:
                biblioteka.append(Ksiazka.from_dict(d))
    except FileNotFoundError:
        biblioteka = []
    return biblioteka