class Aircraft:
    def __init__(self, identifier):
        self.identifier = identifier

    def fly(self):
        raise NotImplementedError("metoda fly musi byc nadpisana")

    def status(self):
        raise NotImplementedError("metoda status musi byc nadpisana")




class PassengerPlane(Aircraft):
    def __init__(self, identifier, passenger_capacity):
        super().__init__(identifier)
        self.passenger_capacity = passenger_capacity

    def fly(self):
        return f"{self.identifier} startuje z max pasażerami: {self.passenger_capacity}"

    def board_passengers(self):
        return f"{self.identifier} przyjmuje pasażerow na poklad."

    def status(self):
        return f"{self.identifier} jest typem pasazerskim"




class CargoPlane(Aircraft):
    def __init__(self, identifier, cargo_weight):
        super().__init__(identifier)
        self.cargo_weight = cargo_weight

    def fly(self):
        return f"{self.identifier} startuje z ladunkiem o wadze: {self.cargo_weight}kg"

    def load_cargo(self):
        return f"{self.identifier} laduje ladunek"

    def status(self):
        return f"{self.identifier} jest samolotem transportowym"




class Helicopter(Aircraft):
    def __init__(self, identifier, rotor_size):
        super().__init__(identifier)
        self.rotor_size = rotor_size

    def fly(self):
        return f"{self.identifier} wystartowal w trybie helikopterowym"

    def hover(self):
        return f"{self.identifier} utrzymuje pozycje w powietrzu"

    def status(self):
        return f"{self.identifier} jest helikopterem"




class Airport:
    def __init__(self, name):
        self.name = name
        self.aircrafts = []


    def add_aircraft(self, aircraft):
        self.aircrafts.append(aircraft)


    def display_aircrafts(self):
        print(f"lotnisko '{self.name}' posiada nastepujace statki powietrzne:")
        for ac in self.aircrafts:
            print(f"- {ac.identifier} ({ac.__class__.__name__}) => {ac.status()}")


    def operate_flights(self):
        print("\noperacje lotnicze:")
        for ac in self.aircrafts:
            print(ac.fly())
            if isinstance(ac, PassengerPlane):
                print(ac.board_passengers())
            elif isinstance(ac, CargoPlane):
                print(ac.load_cargo())
            elif isinstance(ac, Helicopter):
                print(ac.hover())




class Terminal:
    def __init__(self, terminal_id):
        self.terminal_id = terminal_id

    def service(self):
        raise NotImplementedError("metoda service musi byc nadpisana")




class CheckInTerminal(Terminal):
    def service(self):
        return f"terminal {self.terminal_id} przyjmuje pasazerow do odprawy"




class DepartureTerminal(Terminal):
    def service(self):
        return f"terminal {self.terminal_id} przygotowuje odloty"




class ArrivalTerminal(Terminal):
    def service(self):
        return f"terminal {self.terminal_id} obsluguje przyloty"




def main():
    airport1 = Airport("miedzynarodowy port lotniczy")
    pp1 = PassengerPlane("pp-101", 180)
    cp1 = CargoPlane("cp-202", 50000)
    heli1 = Helicopter("heli-303", 12)
    airport1.add_aircraft(pp1)
    airport1.add_aircraft(cp1)
    airport1.add_aircraft(heli1)
    airport1.display_aircrafts()
    airport1.operate_flights()

    terminals = []
    terminals.append(CheckInTerminal("check-1"))
    terminals.append(DepartureTerminal("dep-1"))
    terminals.append(ArrivalTerminal("arr-1"))

    print("\nterminale w lotnisku:")
    for term in terminals:
        print(term.service())
        
    return airport1




def extra_logging():
    print("\nlog systemowy: start procedury diagnostycznej")
    for i in range(3):
        print(f"diagnostyka: krok {i+1} zakonczony")
    print("system lotniska: wszystkie systemy operacyjne dzialaja")
    return




def simulate_delay():
    print("\nsymulacja opoznienia: prosze czekac...")
    for i in range(5):
        print("opoznienie...")
    print("opoznienie zakonczone")
    return




def airport_status(airport_obj):
    print("\nstatus lotniska:")
    airport_obj.display_aircrafts()
    return




def simulate_terminal(term):
    print(f"symulacja dla terminala: {term.terminal_id}")
    print(term.service())
    return




def run_diagnostics():
    print("\ndiagnoza systemu: rozpoczynam diagnoze")
    for _ in range(2):
        print("sprawdzanie systemu...")
    print("diagnoza zakonczona")
    return


def extended_main():
    airport1 = main()
    extra_logging()
    simulate_delay()
    run_diagnostics()
    airport_status(airport1)
    terminals = [CheckInTerminal("check-2"), DepartureTerminal("dep-2"), ArrivalTerminal("arr-2")]
    for term in terminals:
        simulate_terminal(term)
    print("\nkoniec symulacji systemu lotniczego")
    
if __name__ == "__main__":
    main()