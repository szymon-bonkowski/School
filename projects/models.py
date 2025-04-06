import uuid

class Ksiazka:
    def __init__(self, nazwa, liczba_stron):
        self.id = str(uuid.uuid4())
        self.nazwa = nazwa
        self.liczba_stron = liczba_stron

    def to_dict(self):
        return {
            "id": self.id,
            "nazwa": self.nazwa,
            "liczba_stron": self.liczba_stron
        }

    @classmethod
    def from_dict(cls, data):
        ksiazka = cls(data["nazwa"], data["liczba_stron"])
        ksiazka.id = data["id"]
        return ksiazka