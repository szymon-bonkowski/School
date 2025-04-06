class Sigma:
    def __init__(self):
        self.hp = 100
        self.atak = 10
        self.zyje = True
        self.mana = 50
        self.max_hp = 100
        self.max_mana = 50
        self.level = 1
        self.exp = 0
        self.exp_next = 100
        self.zloto = 0
        self.pancerz = 0
        self.kryt_atak = 5
        self.krit_dmg = 2.0
        self.eliksir_zdrowia = 3
        self.eliksir_many = 1

    def odejmij_hp(self, dmg):
        dmg_po_pancerzu = dmg - self.pancerz
        if dmg_po_pancerzu < 0:
            dmg_po_pancerzu = 0
        self.hp -= dmg_po_pancerzu
        if self.hp < 0:
            self.hp = 0
        print(f"sigma dostal {dmg_po_pancerzu} obrazen! zostalo hp: {self.hp}")
        if self.hp == 0:
            self.zyje = False
            print("sigma padl, przegrales...")

    def czy_zyje(self):
        return self.zyje

    def basic_atak(self):
        import random
        if random.randint(1, 100) <= self.kryt_atak:
            dmg = self.atak * self.krit_dmg
            print(f"kryt atak! {dmg} obrazen!")
            return dmg
        return self.atak

    def magic_atak(self):
        if self.mana >= 10:
            self.mana -= 10
            print(f"sigma rzuca magiczny atak! zostala mana: {self.mana}")
            return self.atak * 1.5
        else:
            print("za malo many na magiczny atak!")
            return 0

    def super_atak(self):
        if self.mana >= 25:
            self.mana -= 25
            print(f"sigma wykonuje super atak! zostala mana: {self.mana}")
            return self.atak * 3
        else:
            print("za malo many na super atak!")
            return 0

    def uzyj_eliksir_zdrowia(self):
        if self.eliksir_zdrowia > 0:
            self.eliksir_zdrowia -= 1
            self.hp += 50
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            print(f"sigma wypil eliksir zdrowia! hp: {self.hp}. eliksiry zostaly: {self.eliksir_zdrowia}")
            return True
        else:
            print("nie masz eliksiru zdrowia!")
            return False

    def uzyj_eliksir_many(self):
        if self.eliksir_many > 0:
            self.eliksir_many -= 1
            self.mana += 30
            if self.mana > self.max_mana:
                self.mana = self.max_mana
            print(f"sigma wypil eliksir many! mana: {self.mana}. eliksiry zostaly: {self.eliksir_many}")
            return True
        else:
            print("nie masz eliksiru many!")
            return False

    def dodaj_exp(self, ile):
        self.exp += ile
        print(f"zdobyles {ile} xp!")
        if self.exp >= self.exp_next:
            self.level += 1
            self.exp -= self.exp_next
            self.exp_next = int(self.exp_next * 1.5)
            self.max_hp += 20
            self.hp = self.max_hp
            self.max_mana += 10
            self.mana = self.max_mana
            self.atak += 5
            print(f"level up! sigma jest teraz level {self.level}!")

    def kupuj(self, item):
        if item == "miecz" and self.zloto >= 50:
            self.zloto -= 50
            self.atak += 5
            print(f"kupiono miecz! nowy atak: {self.atak}")
            return True
        elif item == "zbroja" and self.zloto >= 40:
            self.zloto -= 40
            self.pancerz += 2
            print(f"kupiono zbroje! nowy pancerz: {self.pancerz}")
            return True
        elif item == "eliksir_zdrowia" and self.zloto >= 20:
            self.zloto -= 20
            self.eliksir_zdrowia += 1
            print(f"kupiono eliksir zdrowia! masz teraz: {self.eliksir_zdrowia}")
            return True
        elif item == "eliksir_many" and self.zloto >= 25:
            self.zloto -= 25
            self.eliksir_many += 1
            print(f"kupiono eliksir many! masz teraz: {self.eliksir_many}")
            return True
        print("za malo zlota albo zly przedmiot!")
        return False

class Potwor:
    def __init__(self, hp, atak, zloto, xp, nazwa="potwor"):
        self.hp = hp
        self.atak = atak
        self.zyje = True
        self.zloto = zloto
        self.xp = xp
        self.nazwa = nazwa

    def odejmij_hp(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        print(f"{self.nazwa} dostal {dmg} obrazen! zostalo mu hp: {self.hp}")
        if self.hp == 0:
            self.zyje = False
            print(f"{self.nazwa} padl martwy!")

    def czy_zyje(self):
        return self.zyje

    def basic_atak(self):
        return self.atak

class Goblin(Potwor):
    def __init__(self):
        super().__init__(20, 2, 10, 20, "goblin")

class OgromnyGoblin(Potwor):
    def __init__(self):
        super().__init__(60, 8, 35, 60, "ogromny goblin")
        self.szansa_wsciekly = 20

    def basic_atak(self):
        import random
        if random.randint(1, 100) <= self.szansa_wsciekly:
            dmg = self.atak * 2
            print(f"{self.nazwa} robi wsciekly atak! {dmg} obrazen!")
            return dmg
        return self.atak

class Troll(Potwor):
    def __init__(self):
        super().__init__(100, 15, 80, 120, "troll")
        self.regeneracja = True

    def basic_atak(self):
        import random
        return self.atak + random.randint(-3, 3)

    def regeneruj(self):
        if self.regeneracja and self.zyje and self.hp < 100:
            self.hp += 5
            if self.hp > 100:
                self.hp = 100
            print(f"troll regeneruje! hp: {self.hp}")

class Smok(Potwor):
    def __init__(self):
        super().__init__(250, 25, 500, 500, "smok")
        self.ogien = 0

    def basic_atak(self):
        self.ogien += 1
        if self.ogien >= 3:
            self.ogien = 0
            print("smok zieje ogniem!")
            return self.atak * 2
        return self.atak

class Elf(Potwor):
    def __init__(self):
        super().__init__(50, 12, 25, 40, "elf")
        self.szansa_unik = 15

    def basic_atak(self):
        import random
        if random.randint(1, 100) <= self.szansa_unik:
            print(f"{self.nazwa} uniknal ataku!")
            return 0
        return self.atak

class Ork(Potwor):
    def __init__(self):
        super().__init__(80, 18, 50, 70, "ork")
        self.szansa_potezny = 10

    def basic_atak(self):
        import random
        if random.randint(1, 100) <= self.szansa_potezny:
            dmg = self.atak * 1.5
            print(f"{self.nazwa} robi potezny atak! {dmg} obrazen!")
            return dmg
        return self.atak

class Wilkolak(Potwor):
    def __init__(self):
        super().__init__(120, 20, 100, 150, "wilkolak")
        self.regeneracja = True

    def basic_atak(self):
        import random
        return self.atak + random.randint(-5, 5)

    def regeneruj(self):
        if self.regeneracja and self.zyje and self.hp < 120:
            self.hp += 10
            if self.hp > 120:
                self.hp = 120
            print(f"wilkolak regeneruje! hp: {self.hp}")

print("dodano nowe potwory: elf, ork, wilkolak!")

def sklep(s):
    print("\n===== SKLEP =====")
    print("1. miecz (+5 ataku) - 50 zlota")
    print("2. zbroja (+2 pancerza) - 40 zlota")
    print("3. eliksir zdrowia - 20 zlota")
    print("4. eliksir many - 25 zlota")
    print("5. wyjdz ze sklepu")
    print(f"masz zlota: {s.zloto}")
    wybor = input("co kupic? wybierz numer: ")
    items = {"1": "miecz", "2": "zbroja", "3": "eliksir_zdrowia", "4": "eliksir_many"}
    if wybor in items:
        s.kupuj(items[wybor])
    elif wybor == "5":
        print("wychodzisz ze sklepu.")
    else:
        print("zla opcja!")

def walka(s, p):
    print("\n=== WALKA START ===")
    while p.czy_zyje() and s.czy_zyje():
        print(f"\ntwoja tura! level: {s.level}, hp: {s.hp}/{s.max_hp}, mana: {s.mana}/{s.max_mana}")
        print("1. normalny atak\n2. magiczny atak (10 many)\n3. super atak (25 many)")
        print("4. uzyj eliksiru zdrowia\n5. uzyj eliksiru many")
        opcja = input("wybierz opcje (1-5): ")
        if opcja == "1":
            p.odejmij_hp(s.basic_atak())
        elif opcja == "2":
            dmg = s.magic_atak()
            if dmg > 0:
                p.odejmij_hp(dmg)
        elif opcja == "3":
            dmg = s.super_atak()
            if dmg > 0:
                p.odejmij_hp(dmg)
        elif opcja == "4":
            s.uzyj_eliksir_zdrowia()
        elif opcja == "5":
            s.uzyj_eliksir_many()
        else:
            print("zla opcja, tracisz ture!")
        if p.czy_zyje():
            print("\ntura przeciwnika!")
            s.odejmij_hp(p.basic_atak())
            if isinstance(p, Troll):
                p.regeneruj()
            if isinstance(p, Wilkolak):
                p.regeneruj()
    if s.czy_zyje():
        import random
        zl = max(0, p.zloto + random.randint(-5, 5))
        print(f"wygrales! dostajesz {zl} zlota i {p.xp} xp!")
        s.zloto += zl
        s.dodaj_exp(p.xp)
        s.hp = s.max_hp
        s.mana = s.max_mana
        s.eliksir_zdrowia = 3
        s.eliksir_many = 1
        return True
    else:
        print("przegrales! koniec gry.")
        return False

player = Sigma()
zabite = {"gobliny": 0, "ogromne gobliny": 0, "trolle": 0, "smoki": 0, "elfy": 0, "orki": 0, "wilkolaki": 0}

print("=== WITAJ W GRZE RPG ===\nJestes mega wojownikiem o imieniu sigma!")
gra = True
while gra and player.czy_zyje():
    print("\n=== MENU GLOWNE ===")
    print("1. walcz z goblinem")
    print("2. walcz z ogromnym goblinem")
    print("3. walcz z trollem")
    print("4. walcz ze smokiem (boss)")
    print("5. walcz z elfem")
    print("6. walcz z orkiem")
    print("7. walcz z wilkolakiem")
    print("8. odwiedz sklep")
    print("9. pokaz statystyki")
    print("10. koniec gry")
    opcja = input("co chcesz zrobic? ")
    if opcja == "1":
        if walka(player, Goblin()):
            zabite["gobliny"] += 1
    elif opcja == "2":
        if player.level >= 2:
            if walka(player, OgromnyGoblin()):
                zabite["ogromne gobliny"] += 1
        else:
            print("musisz byc na levelu 2, zeby walczyc z ogromnym goblinem!")
    elif opcja == "3":
        if player.level >= 3:
            if walka(player, Troll()):
                zabite["trolle"] += 1
        else:
            print("musisz byc na levelu 3, zeby walczyc z trollem!")
    elif opcja == "4":
        if player.level >= 5:
            if walka(player, Smok()):
                zabite["smoki"] += 1
                print("super, pokonales smoka!")
        else:
            print("musisz byc na levelu 5, zeby walczyc ze smokiem!")
    elif opcja == "5":
        if walka(player, Elf()):
            zabite["elfy"] += 1
    elif opcja == "6":
        if walka(player, Ork()):
            zabite["orki"] += 1
    elif opcja == "7":
        if walka(player, Wilkolak()):
            zabite["wilkolaki"] += 1
    elif opcja == "8":
        sklep(player)
    elif opcja == "9":
        print("\n=== STATYSTYKI GRacza ===")
        print(f"level: {player.level}, xp: {player.exp}/{player.exp_next}")
        print(f"hp: {player.hp}/{player.max_hp}, mana: {player.mana}/{player.max_mana}")
        print(f"atak: {player.atak}, pancerz: {player.pancerz}, zloto: {player.zloto}")
        print(f"eliksiry zdrowia: {player.eliksir_zdrowia}, eliksiry many: {player.eliksir_many}")
        print("\n=== ZABITE POTWORY ===")
        for k, v in zabite.items():
            print(f"{k}: {v}")
    elif opcja == "10":
        gra = False
        print("koniec gry! dziekujemy!")
    else:
        print("zla opcja!")
print("\n=== STATYSTYKI KONCOWE ===")
print(f"osiagniety level: {player.level}, zloto: {player.zloto}")
for k, v in zabite.items():
    print(f"{k}: {v}")
print(f"calosc zabitych potworow: {sum(zabite.values())}")
print("=== KONIEC ===")