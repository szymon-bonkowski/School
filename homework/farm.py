class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        raise NotImplementedError("Ta metoda musi być nadpisana przez podklasę")


class Cow(Animal):
    def __init__(self, name, milk_production):
        super().__init__(name)
        self.milk_production = milk_production

    def make_sound(self):
        return "Muuu"

    def produce_milk(self):
        return f"{self.name} produkuje {self.milk_production} litrów mleka dziennie."


class Chicken(Animal):
    def __init__(self, name):
        super().__init__(name)

    def make_sound(self):
        return "Kurku, kurku"

    def lay_egg(self):
        return f"{self.name} zniosła jajko!"


class Pig(Animal):
    def __init__(self, name):
        super().__init__(name)

    def make_sound(self):
        return "Chrum"

    def roll_in_mud(self):
        return f"{self.name} tarza się w błocie!"


class Farm:
    def __init__(self, name):
        self.name = name
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def show_animals(self):
        print(f"Zwierzęta na farmie '{self.name}':")
        for animal in self.animals:
            print(f"- {animal.name} ({animal.__class__.__name__}) mówi: {animal.make_sound()}")

    def farm_activity(self):
        print("\nAktywności na farmie:")
        for animal in self.animals:
            if isinstance(animal, Cow):
                print(animal.produce_milk())
            elif isinstance(animal, Chicken):
                print(animal.lay_egg())
            elif isinstance(animal, Pig):
                print(animal.roll_in_mud())


class Plant:
    def __init__(self, name):
        self.name = name

    def grow(self):
        return self.name + " rośnie."


class Ziemniak(Plant):
    def grow(self):
        return self.name + " rośnie szybko, bo to ziemniak."


class Marchew(Plant):
    def grow(self):
        return self.name + " rośnie powoli, ale jest zdrowa."


class Burak(Plant):
    def grow(self):
        return self.name + " rośnie i już zbiera się z niego burak."


def main():
    my_farm = Farm("Szczęśliwa Farma")
    cow1 = Cow("Bessie", 25)
    chicken1 = Chicken("Koko")
    pig1 = Pig("Porky")
    my_farm.add_animal(cow1)
    my_farm.add_animal(chicken1)
    my_farm.add_animal(pig1)
    my_farm.show_animals()
    my_farm.farm_activity()

    plants = []
    plants.append(Ziemniak("Ziemniak1"))
    plants.append(Marchew("Marchew1"))
    plants.append(Burak("Burak1"))

    print("\nRośliny na farmie:")
    for plant in plants:
        print(plant.grow())


if __name__ == "__main__":
    main()