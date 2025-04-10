class PassengerService:
    def __init__(self, passenger_capacity):
        self.passenger_capacity = passenger_capacity

    def fly(self, identifier):
        return f"{identifier} startuje z max pasażerami: {self.passenger_capacity}"

    def operate(self, identifier):
        return f"{identifier} przyjmuje pasażerow na poklad."

    def status(self, identifier):
        return f"{identifier} jest typem pasazerskim"




class CargoService:
    def __init__(self, cargo_weight):
        self.cargo_weight = cargo_weight

    def fly(self, identifier):
        return f"{identifier} startuje z ladunkiem o wadze: {self.cargo_weight}kg"

    def operate(self, identifier):
        return f"{identifier} laduje ladunek"

    def status(self, identifier):
        return f"{identifier} jest samolotem transportowym"




class HeliService:
    def __init__(self, rotor_size):
        self.rotor_size = rotor_size

    def fly(self, identifier):
        return f"{identifier} wystartowal w trybie helikopterowym"

    def operate(self, identifier):
        return f"{identifier} utrzymuje pozycje w powietrzu"

    def status(self, identifier):
        return f"{identifier} jest helikopterem"




class Aircraft:
    def __init__(self, identifier, service, aircraft_type):
        self.identifier = identifier
        self.service = service
        self.aircraft_type = aircraft_type

    def fly(self):
        return self.service.fly(self.identifier)

    def operate(self):
        return self.service.operate(self.identifier)

    def status(self):
        return self.service.status(self.identifier)






class CheckInService:
    def info(self, terminal_id):
        return f"terminal {terminal_id} przyjmuje pasazerow do odprawy"




class DepartureService:
    def info(self, terminal_id):
        return f"terminal {terminal_id} przygotowuje odloty"




class ArrivalService:
    def info(self, terminal_id):
        return f"terminal {terminal_id} obsluguje przyloty"




class Terminal:
    def __init__(self, terminal_id, service):
        self.terminal_id = terminal_id
        self.service = service

    def service_info(self):
        return self.service.info(self.terminal_id)





class Airport:
    def __init__(self, name):
        self.name = name
        self.aircrafts = []


    def add_aircraft(self, aircraft):
        self.aircrafts.append(aircraft)


    def display_aircrafts(self):
        print(f"lotnisko '{self.name}' posiada nastepujace statki powietrzne:")
        for ac in self.aircrafts:
            print(f"- {ac.identifier} ({ac.aircraft_type}) => {ac.status()}")




    def operate_flights(self):
        print("\noperacje lotnicze:")
        for ac in self.aircrafts:
            print(ac.fly())
            print(ac.operate())




def main():
    global airport1
    airport1 = Airport("miedzynarodowy port lotniczy")
    ps = PassengerService(180)
    cs = CargoService(50000)
    hs = HeliService(12)
    ac1 = Aircraft("pp-101", ps, "PassengerPlane")
    ac2 = Aircraft("cp-202", cs, "CargoPlane")
    ac3 = Aircraft("heli-303", hs, "Helicopter")
    airport1.add_aircraft(ac1)
    airport1.add_aircraft(ac2)
    airport1.add_aircraft(ac3)
    airport1.display_aircrafts()
    airport1.operate_flights()

    term1 = Terminal("check-1", CheckInService())
    term2 = Terminal("dep-1", DepartureService())
    term3 = Terminal("arr-1", ArrivalService())
    terminals = [term1, term2, term3]

    print("\nterminale w lotnisku:")
    for term in terminals:
        print(term.service_info())




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
    print(term.service_info())
    return




def run_diagnostics():
    print("\ndiagnoza systemu: rozpoczynam diagnoze")
    for _ in range(2):
        print("sprawdzanie systemu...")
    print("diagnoza zakonczona")
    return




def extended_main():
    main()
    extra_logging()
    simulate_delay()
    run_diagnostics()
    airport_status(airport1)
    terms = [
        Terminal("check-2", CheckInService()),
        Terminal("dep-2", DepartureService()),
        Terminal("arr-2", ArrivalService())
    ]
    for term in terms:
        simulate_terminal(term)
    print("\nkoniec symulacji systemu lotniczego")
    return

if __name__ == "__main__":
    main()